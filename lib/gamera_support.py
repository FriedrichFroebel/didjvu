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
Bridge to the Gamera framework
"""

import collections
import ctypes
import math
import re
import sys

from lib import utils

try:
    from PIL import Image as PILImage
except ImportError as _exception:  # no coverage
    utils.enhance_import_error(
        _exception,
        'Pillow',
        'python3-pil',
        'https://pypi.org/project/Pillow/'
    )
    raise

try:
    import gamera
except ImportError as _exception:  # no coverage
    utils.enhance_import_error(
        _exception,
        'Gamera',
        '',
        'https://github.com/hsnr-gamera/gamera-4'
    )
    raise
del gamera  # quieten pyflakes


from gamera import __version__ as version  # noqa: E402
from gamera.core import load_image as _load_image  # noqa: E402
from gamera.core import init_gamera as _init  # noqa: E402
from gamera.core import Image, RGB, GREYSCALE, ONEBIT, Point, Dim, RGBPixel  # noqa: E402
from gamera.plugins.pil_io import from_pil as _from_pil  # noqa: E402
import gamera.args  # noqa: E402


def has_version(*required_version):
    return tuple(map(int, version.split('.'))) >= required_version


def load_image(filename):
    pil_image = PILImage.open(filename)
    dpi_x, dpi_y = pil_image.info.get('dpi', (0, 0))
    if dpi_x <= 1 or dpi_y <= 1:
        # Not reliable
        dpi = None
    else:
        dpi = int(round(
            math.hypot(dpi_x, dpi_y) / math.hypot(1, 1)
        ))
    try:
        if pil_image.format == 'TIFF':
            # Gamera handles only a few TIFF color modes correctly.
            # https://bugs.debian.org/784374
            gamera_modes = ['1', 'I;16', 'L', 'RGB']
        elif pil_image.format == 'PNG':
            # Gamera doesn't handle 16-bit greyscale PNG images correctly.
            # https://groups.yahoo.com/neo/groups/gamera-devel/conversations/messages/2425
            gamera_modes = ['1', 'L', 'RGB']
        else:
            gamera_modes = []
        if pil_image.mode not in gamera_modes:
            raise IOError
        # Gamera supports more TIFF compression formats that PILImage.
        # https://mail.python.org/pipermail/image-sig/2003-July/002354.html
        image = _load_image(filename)
    except IOError:
        # Gamera supports importing only 8-bit and RGB from PILImage:
        if pil_image.mode[:2] in {'1', '1;', 'I', 'I;', 'L;'}:
            pil_image = pil_image.convert('L')
        elif pil_image.mode not in {'RGB', 'L'}:
            pil_image = pil_image.convert('RGB')
        assert pil_image.mode in {'RGB', 'L'}
        # noinspection PyArgumentList
        image = _from_pil(pil_image)
    image.dpi = dpi
    pil_image.close()
    return image


class Argument:
    _type_map = {
        gamera.args.Int: int,
        gamera.args.Real: float,
        gamera.args.Check: bool,
    }

    def __init__(self, arg):
        self.name = arg.name.replace(' ', '-').replace('_', '-')
        for gtype, ptype in self._type_map.items():
            if isinstance(arg, gtype):
                self.type = ptype
                break
        else:
            raise NotImplementedError(f'argument {self.name}: unsupported type {arg!r}')  # no coverage
        if self.type in {int, float}:
            self.min, self.max = arg.rng
            if self.min == -gamera.args.DEFAULT_MAX_ARG_NUMBER:
                self.min = None
            if self.max == gamera.args.DEFAULT_MAX_ARG_NUMBER:
                self.max = None
        else:
            self.min = self.max = None
        self.has_default = arg.has_default
        self.default = arg.default
        if isinstance(self.default, gamera.args.CNoneDefault):
            self.default = None
        elif self.has_default:
            if not isinstance(self.default, self.type):
                raise TypeError(
                    f'argument {self.name}: type({self.default!r}) should be {self.type.__name__}'
                )  # no coverage
        else:
            self.default = None


class Plugin:
    def __init__(self, plugin, name):
        self._plugin = plugin
        self._pixel_types = plugin.self_type.pixel_types
        self._method = None
        self.name = name
        self.args = collections.OrderedDict()
        for arg in plugin.args:
            if arg.name == 'storage format':
                continue
            arg = Argument(arg)
            self.args[arg.name] = arg

    def __call__(self, image, **kwargs):
        kwargs = {
            key.replace('-', '_'): value
            for key, value
            in kwargs.items()
        }
        pixel_types = self._pixel_types
        if image.data.pixel_type not in pixel_types:
            if RGB in pixel_types:
                image = image.to_rgb()
            elif GREYSCALE in pixel_types:
                image = image.to_greyscale()
            else:
                raise NotImplementedError(
                    f'method {self.name} does not support pixel type {image.pixel_type_name}'
                )  # no coverage
        assert image.data.pixel_type in pixel_types
        if self._method is None:
            self._method = self._plugin()
        return self._method(image, **kwargs)


def _load_methods():
    replace_suffix = re.compile(r'_threshold$').sub

    # noinspection PyUnresolvedReferences
    class MethodsContainer:
        from gamera.plugins.threshold import abutaleb_threshold
        from gamera.plugins.threshold import bernsen_threshold
        from gamera.plugins.threshold import djvu_threshold
        from gamera.plugins.threshold import otsu_threshold
        from gamera.plugins.threshold import threshold as global_threshold
        from gamera.plugins.threshold import tsai_moment_preserving_threshold as tsai
        # TODO: from gamera.plugins.binarization import gatos_threshold
        from gamera.plugins.binarization import brink_threshold
        from gamera.plugins.binarization import niblack_threshold
        from gamera.plugins.binarization import sauvola_threshold
        from gamera.plugins.binarization import shading_subtraction
        from gamera.plugins.binarization import white_rohrer_threshold

    method_mapping = dict()
    for name, plugin in vars(MethodsContainer).items():
        if name.startswith('_'):
            continue
        name = replace_suffix('', name)
        name = name.replace('_', '-')
        method = Plugin(plugin, name)
        method_mapping[name] = method
    return method_mapping


methods = _load_methods()


def to_pil_rgb(image):
    # About 20% faster than the standard .to_pil() method of Gamera 3.2.6.
    buffer = ctypes.create_string_buffer(3 * image.ncols * image.nrows)
    image.to_buffer(buffer)
    return PILImage.frombuffer('RGB', (image.ncols, image.nrows), buffer, 'raw', 'RGB', 0, 1)


def to_pil_1bpp(image):
    if image.data.pixel_type != GREYSCALE:
        image = image.to_greyscale()
    return image.to_pil()


def init():
    if not has_version(4, 0):
        raise RuntimeError('Gamera >= 4.0 is required')
    blocked_numpy = False
    if 'numpy' not in sys.modules:
        # noinspection PyTypeChecker
        sys.modules['numpy'] = None
        blocked_numpy = True
    try:
        result = _init()
    finally:
        if blocked_numpy:
            del sys.modules['numpy']
    return result


__all__ = [
    # classes:
    'Dim',
    'Image',
    'Point',
    'RGBPixel',
    # pixel types:
    'ONEBIT',
    'GREYSCALE',
    'RGB',
    # functions:
    'init',
    'load_image',
    'methods',
    'to_pil_1bpp',
    'to_pil_rgb',
]

# vim:ts=4 sts=4 sw=4 et
