# encoding=UTF-8

# Copyright © 2009-2021 Jakub Wilk <jwilk@jwilk.net>
#
# This file is part of didjvu.
#
# didjvu is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# didjvu is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details.

"""
didjvu core
"""

import itertools
import logging
import os
import sys

from lib import cli
from lib import djvu_support
from lib import filetype
from lib import fs
from lib import gamera_support
from lib import ipc
from lib import templates
from lib import temporary
from lib import utils
from lib import xmp

logger = None


def setup_logging():
    global logger
    logger = logging.getLogger('didjvu.main')
    ipc_logger = logging.getLogger('didjvu.ipc')
    logging.NOSY = (logging.INFO + logging.DEBUG) // 2
    # noinspection PyUnresolvedReferences
    assert logging.INFO > logging.NOSY > logging.DEBUG

    def nosy(msg, *args, **kwargs):
        # noinspection PyUnresolvedReferences
        logger.log(logging.NOSY, msg, *args, **kwargs)

    logger.nosy = nosy
    # Main handler:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    # IPC handler:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('+ %(message)s')
    handler.setFormatter(formatter)
    ipc_logger.addHandler(handler)


def error(message, *args, **kwargs):
    if args or kwargs:
        message = message.format(*args, **kwargs)
    print(f'didjvu: error: {message}', file=sys.stderr)
    sys.exit(1)


def parallel_for(options, function, *iterables):
    for args in zip(*iterables):
        function(options, *args)


def check_tty():
    if sys.stdout.isatty():
        error('refusing to write binary data to a terminal')


def get_subsampled_dimensions(image, subsample):
    width = (image.ncols + subsample - 1) // subsample
    height = (image.nrows + subsample - 1) // subsample
    return gamera_support.Dim(width, height)


def subsample_foreground(image, mask, options):
    # TODO: Optimize, perhaps using Cython.
    ratio = options.subsample
    subsampled_size = get_subsampled_dimensions(mask, ratio)
    mask = mask.to_greyscale()
    mask = mask.threshold(254)
    mask = mask.erode()
    subsampled_image = gamera_support.Image((0, 0), subsampled_size, pixel_type=gamera_support.RGB)
    subsampled_mask = gamera_support.Image((0, 0), subsampled_size, pixel_type=gamera_support.ONEBIT)
    y0 = 0
    width, height = image.ncols, image.nrows
    image = image.to_rgb()
    image_get = image.get
    mask_get = mask.get
    subsampled_image_set = subsampled_image.set
    subsampled_mask_set = subsampled_mask.set
    for sy in range(0, subsampled_image.nrows):
        x0 = 0
        for sx in range(0, subsampled_image.ncols):
            n = r = g = b = 0
            y = y0
            for dy in range(ratio):
                if y >= height:
                    break
                x = x0
                for dx in range(ratio):
                    if x >= width:
                        break
                    pt = gamera_support.Point(x, y)
                    if mask_get(pt):
                        n += 1
                        pixel = image_get(pt)
                        r += pixel.red
                        g += pixel.green
                        b += pixel.blue
                    x += 1
                y += 1
            pt = gamera_support.Point(sx, sy)
            if n > 0:
                r = (r + n // 2) // n
                g = (g + n // 2) // n
                b = (b + n // 2) // n
                subsampled_image_set(pt, gamera_support.RGBPixel(r, g, b))
            else:
                subsampled_mask_set(pt, 1)
            x0 += ratio
        y0 += ratio
    return subsampled_image, subsampled_mask


def subsample_background(image, mask, options):
    dim = get_subsampled_dimensions(mask, options.subsample)
    mask = mask.to_greyscale()
    mask = mask.resize(dim, 0)
    mask = mask.dilate().dilate()
    mask = mask.threshold(254)
    image = image.resize(dim, 1)
    return image, mask


def make_layer(image, mask, subsampler, options):
    image, mask = subsampler(image, mask, options)
    return djvu_support.photo_to_djvu(
        image=gamera_support.to_pil_rgb(image),
        mask_image=gamera_support.to_pil_1bpp(mask),
        slices=options.slices,
        crcb=options.crcb
    )


def image_dpi(image, options):
    dpi = options.dpi
    if dpi is None:
        dpi = image.dpi
    if dpi is None:
        dpi = djvu_support.DPI_DEFAULT
    dpi = max(dpi, djvu_support.DPI_MIN)
    dpi = min(dpi, djvu_support.DPI_MAX)
    return dpi


def image_to_djvu(width, height, image, mask, options):
    dpi = image_dpi(image, options)
    loss_level = options.loss_level
    if options.pages_per_dict > 1:
        # XXX This should probably go the other way round: we run minidjvu
        # first, and then reuse its masks.
        loss_level = 0
    sjbz = djvu_support.bitonal_to_djvu(gamera_support.to_pil_1bpp(mask), loss_level=loss_level)
    if options.fg_bg_defaults:
        image = gamera_support.to_pil_rgb(image)
        return djvu_support.Multichunk(width, height, dpi, image=image, sjbz=sjbz)
    else:
        chunks = dict(sjbz=sjbz)
        if options.foreground_options.slices != [0]:
            foreground_djvu = make_layer(image, mask, subsample_foreground, options.foreground_options)
            chunks.update(fg44=djvu_support.djvu_to_iw44(foreground_djvu))
        if options.background_options.slices != [0]:
            background_djvu = make_layer(image, mask, subsample_background, options.background_options)
            chunks.update(bg44=djvu_support.djvu_to_iw44(background_djvu))
        return djvu_support.Multichunk(width, height, dpi, **chunks)


def generate_mask(filename, image, method, kwargs):
    """
    Generate mask using the provided method (if filename is not None);
    or simply load it from file (if filename is not None).
    """
    if filename is None:
        return method(image, **kwargs)
    else:
        return gamera_support.load_image(filename)


def format_compression_info(bytes_in, bytes_out, bits_per_pixel):
    ratio = 1.0 * bytes_in / bytes_out
    percent_saved = (1.0 * bytes_in - bytes_out) * 100 / bytes_in
    msg = (
        f'{bits_per_pixel:.3f} bits/pixel; '
        f'{ratio:.3f}:1, {percent_saved:.2f}% saved, '
        f'{bytes_in} bytes in, {bytes_out} bytes out'
    )
    return msg


class Main:
    def __init__(self):
        parser = cli.ArgumentParser(gamera_support.methods, default_method='djvu')
        parser.parse_arguments(actions=self)

    def check_common(self, options):
        if len(options.masks) == 0:
            options.masks = [None for _ in options.input]
        elif len(options.masks) != len(options.input):
            error(
                'the number of input images ({0}) does not match the number of masks ({1})',
                len(options.input),
                len(options.masks)
            )
        setup_logging()
        ipc_logger = logging.getLogger('didjvu.ipc')
        assert logger is not None
        # noinspection PyUnresolvedReferences
        log_level = {
            0: logging.WARNING,
            1: logging.INFO,
            2: logging.NOSY,
        }.get(options.verbosity, logging.DEBUG)
        # noinspection PyUnresolvedReferences
        logger.setLevel(log_level)
        ipc_logger.setLevel(log_level)
        djvu_support.require_cli()
        gamera_support.init()

    def check_multi_output(self, options):
        self.check_common(options)
        page_id_memo = {}
        if options.output is None:
            if options.output_template is not None:
                options.output = [
                    templates.expand(options.output_template, image_path, image_index, page_id_memo)
                    for image_index, image_path in enumerate(options.input)
                ]
                options.xmp_output = [f'{output_name}.xmp' if options.xmp else None for output_name in options.output]
            elif len(options.input) == 1:
                options.output = [sys.stdout]
                options.xmp_output = [None]
                check_tty()
            else:
                error('cannot output multiple files to stdout')
        else:
            if len(options.input) == 1:
                options.xmp_output = [f'{options.output}.xmp'] if options.xmp else [None]
                options.output = [options.output]
            else:
                error('cannot output multiple files to a single file')
        assert len(options.masks) == len(options.output) == len(options.input)
        options.output = (
            open(file_or_path, 'wb') if isinstance(file_or_path, str) else file_or_path
            for file_or_path in options.output
        )
        options.xmp_output = (
            open(file_or_path, 'wb') if isinstance(file_or_path, str) else file_or_path
            for file_or_path in options.xmp_output
        )

    def check_single_output(self, options):
        self.check_common(options)
        if options.output is None:
            options.output = [sys.stdout]
            options.xmp_output = [None]
            check_tty()
        else:
            filename = options.output
            # noinspection PyTypeChecker
            options.output = [open(filename, 'wb')]
            options.xmp_output = [open(f'{filename}.xmp', 'wb')] if options.xmp else [None]
        assert len(options.output) == len(options.xmp_output) == 1

    def encode(self, options):
        self.check_multi_output(options)
        parallel_for(options, self.encode_one, options.input, options.masks, options.output, options.xmp_output)

    def encode_one(self, options, image_filename, mask_filename, output, xmp_output):
        bytes_in = os.path.getsize(image_filename)
        # noinspection PyUnresolvedReferences
        logger.info(f'{image_filename}:')
        file_type = filetype.check(image_filename)
        if file_type.like(filetype.Djvu):
            if file_type.like(filetype.DjvuSingle):
                # noinspection PyUnresolvedReferences
                logger.info('- copying DjVu as is')
                with open(image_filename, 'rb') as djvu_file:
                    fs.copy_file(djvu_file, output)
            else:
                # TODO: Figure out how many pages the multi-page document
                #       consists of. If it's only one, continue.
                error('multi-page DjVu documents are not supported as input files')
            return
        # noinspection PyUnresolvedReferences
        logger.info('- reading image')
        image = gamera_support.load_image(image_filename)
        width, height = image.ncols, image.nrows
        # noinspection PyUnresolvedReferences
        logger.nosy(f'- image size: {width} x {height}')
        mask = generate_mask(mask_filename, image, options.method, options.parameters)
        n_connected_components = -1
        if xmp_output:
            n_connected_components = len(mask.cc_analysis())
        # noinspection PyUnresolvedReferences
        logger.info('- converting to DjVu')
        djvu_doc = image_to_djvu(width, height, image, mask, options=options)
        djvu_file = djvu_doc.save()
        try:
            bytes_out = fs.copy_file(djvu_file, output)
        finally:
            djvu_file.close()
        bits_per_pixel = 8.0 * bytes_out / (width * height)
        compression_info = format_compression_info(bytes_in, bytes_out, bits_per_pixel)
        # noinspection PyUnresolvedReferences
        logger.info(f'- {compression_info}')
        if xmp_output:
            # noinspection PyUnresolvedReferences
            logger.info('- saving XMP metadata')
            metadata = xmp.metadata()
            metadata.import_(image_filename)
            internal_properties = list(cli.dump_options(options)) + [
                ('n-connected-components', str(n_connected_components))
            ]
            metadata.update(
                media_type='image/vnd.djvu',
                internal_properties=internal_properties,
            )
            metadata.write(xmp_output)

    def separate_one(self, options, image_filename, output):
        # noinspection PyUnresolvedReferences
        logger.info(f'{image_filename}:')
        file_type = filetype.check(image_filename)
        if file_type.like(filetype.Djvu):
            # TODO: Figure out how many pages the document consists of.
            #       If it's only one, extract the existing mask.
            error('DjVu documents are not supported as input files')
        # noinspection PyUnresolvedReferences
        logger.info('- reading image')
        image = gamera_support.load_image(image_filename)
        width, height = image.ncols, image.nrows
        # noinspection PyUnresolvedReferences
        logger.nosy(f'- image size: {width} x {height}')
        # noinspection PyUnresolvedReferences
        logger.info('- thresholding')
        mask = generate_mask(None, image, options.method, options.parameters)
        # noinspection PyUnresolvedReferences
        logger.info('- saving')
        if output is not sys.stdout:
            # A real file
            mask.save_PNG(output.name)
        else:
            tmp_output = temporary.file(suffix='.png')
            try:
                mask.save_PNG(tmp_output.name)
                fs.copy_file(tmp_output, output)
            finally:
                tmp_output.close()

    def separate(self, options):
        self.check_multi_output(options)
        for mask in options.masks:
            assert mask is None
        parallel_for(options, self.separate_one, options.input, options.output)

    def bundle(self, options):
        self.check_single_output(options)
        if (options.pages_per_dict <= 1) or (len(options.input) <= 1):
            self.bundle_simple(options)
        else:
            ipc.require('minidjvu')
            self.bundle_complex(options)
        [xmp_output] = options.xmp_output
        if xmp_output:
            # noinspection PyUnresolvedReferences
            logger.info('saving XMP metadata')
            metadata = xmp.metadata()
            internal_properties = list(cli.dump_options(options, multi_page=True))
            metadata.update(
                media_type='image/vnd.djvu',
                internal_properties=internal_properties,
            )
            metadata.write(xmp_output)

    def _bundle_simple_page(self, o, input_file, mask, component_name):
        with open(component_name, 'wb') as component:
            self.encode_one(o, input_file, mask, component, None)

    def bundle_simple(self, options):
        [output] = options.output
        with temporary.directory() as tmpdir:
            bytes_in = 0
            component_filenames = []
            page_id_memo = {}
            for page, (input_file, mask) in enumerate(zip(options.input, options.masks)):
                bytes_in += os.path.getsize(input_file)
                page_id = templates.expand(options.page_id_template, input_file, page, page_id_memo)
                try:
                    djvu_support.validate_page_id(page_id)
                except ValueError as exception:
                    error(exception)
                component_filenames += [os.path.join(tmpdir, page_id)]
            parallel_for(options, self._bundle_simple_page, options.input, options.masks, component_filenames)
            # noinspection PyUnresolvedReferences
            logger.info('bundling')
            djvu_file = djvu_support.bundle_djvu(*component_filenames)
            try:
                bytes_out = fs.copy_file(djvu_file, output)
            finally:
                djvu_file.close()
        bits_per_pixel = float('nan')  # FIXME!
        compression_info = format_compression_info(bytes_in, bytes_out, bits_per_pixel)
        # noinspection PyUnresolvedReferences
        logger.nosy(compression_info)

    def _bundle_complex_page(self, options, page, minidjvu_in_dir, image_filename, mask_filename, pixels):
        # noinspection PyUnresolvedReferences
        logger.info(f'{image_filename}:')
        file_type = filetype.check(image_filename)
        if file_type.like(filetype.Djvu):
            # TODO: Allow merging existing documents (even multi-page ones).
            error('DjVu documents are not supported as input files')
        # noinspection PyUnresolvedReferences
        logger.info('- reading image')
        image = gamera_support.load_image(image_filename)
        dpi = image_dpi(image, options)
        width, height = image.ncols, image.nrows
        pixels[0] += width * height
        # noinspection PyUnresolvedReferences
        logger.nosy(f'- image size: {width} x {height}')
        mask = generate_mask(mask_filename, image, options.method, options.parameters)
        # noinspection PyUnresolvedReferences
        logger.info('- converting to DjVu')
        page.djvu = image_to_djvu(width, height, image, mask, options=options)
        del image, mask
        page.sjbz = djvu_support.Multichunk(width, height, dpi, sjbz=page.djvu['sjbz'])
        page.sjbz_symlink = os.path.join(minidjvu_in_dir, page.page_id)
        os.symlink(page.sjbz.save().name, page.sjbz_symlink)

    def bundle_complex(self, options):
        [output] = options.output
        with temporary.directory() as minidjvu_in_dir:
            bytes_in = 0
            pixels = [0]
            page_info = []
            page_id_memo = {}
            for page_number, (image_filename, mask_filename) in enumerate(zip(options.input, options.masks)):
                page = utils.Namespace()
                page_info += [page]
                bytes_in += os.path.getsize(image_filename)
                page.page_id = templates.expand(options.page_id_template, image_filename, page_number, page_id_memo)
                try:
                    djvu_support.validate_page_id(page.page_id)
                except ValueError as exception:
                    error(exception)
            del page  # quieten pyflakes
            parallel_for(
                options,
                self._bundle_complex_page,
                page_info,
                itertools.repeat(minidjvu_in_dir),
                options.input,
                options.masks,
                itertools.repeat(pixels)
            )
            [pixels] = pixels
            with temporary.directory() as minidjvu_out_dir:
                # noinspection PyUnresolvedReferences
                logger.info('creating shared dictionaries')

                def chdir():
                    os.chdir(minidjvu_out_dir)

                arguments = [
                    'minidjvu',
                    '--indirect',
                    '--pages-per-dict', str(options.pages_per_dict),
                ]
                if options.loss_level > 0:
                    arguments += ['--aggression', str(options.loss_level)]
                assert len(page_info) > 1  # minidjvu won't create single-page indirect documents
                arguments += [page.sjbz_symlink for page in page_info]
                index_filename = temporary.name(prefix='__index__.', suffix='.djvu', dir=minidjvu_out_dir)
                index_filename = os.path.basename(index_filename)  # FIXME: Name conflicts are still possible!
                arguments += [index_filename]
                ipc.Subprocess(arguments, preexec_fn=chdir).wait()
                os.remove(os.path.join(minidjvu_out_dir, index_filename))
                component_filenames = []
                for page_number, page in enumerate(page_info):
                    if page_number % options.pages_per_dict == 0:
                        iff_name = fs.replace_ext(page_info[page_number].page_id, 'iff')
                        iff_name = os.path.join(minidjvu_out_dir, iff_name)
                        component_filenames += [iff_name]
                    sjbz_name = os.path.join(minidjvu_out_dir, page.page_id)
                    component_filenames += [sjbz_name]
                    page.djvu['sjbz'] = sjbz_name
                    page.djvu['incl'] = iff_name
                    page.djvu = page.djvu.save()
                    page.djvu_symlink = os.path.join(minidjvu_out_dir, page.page_id)
                    os.unlink(page.djvu_symlink)
                    os.symlink(page.djvu.name, page.djvu_symlink)
                # noinspection PyUnresolvedReferences
                logger.info('bundling')
                djvu_file = djvu_support.bundle_djvu(*component_filenames)
                try:
                    bytes_out = fs.copy_file(djvu_file, output)
                finally:
                    djvu_file.close()
        bits_per_pixel = 8.0 * bytes_out / pixels
        compression_info = format_compression_info(bytes_in, bytes_out, bits_per_pixel)
        # noinspection PyUnresolvedReferences
        logger.nosy(compression_info)


__all__ = ['Main']

# vim:ts=4 sts=4 sw=4 et
