# encoding=UTF-8

# Copyright © 2015 Jakub Wilk <jwilk@jwilk.net>
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

import glob
import os
import re

from tests.tools import TestCase

from PIL import Image

from lib import gamera_support


class LoadImageTestCase(TestCase):
    def _test_load_image(self, filename):
        dpi_match = re.search(r'dpi(\d+)', filename)
        path = self.get_data_file(filename)
        gamera_support.init()
        image = gamera_support.load_image(path)
        self.assertIsInstance(image, gamera_support.Image)
        if dpi_match is None:
            self.assertIsNone(image.dpi)
        else:
            dpi = int(dpi_match.group(1))
            self.assertIsInstance(image.dpi, int)
            self.assertEqual(image.dpi, dpi)

    def test_load_image(self):
        paths = []
        for extension in ['tiff', 'png', 'pgm', 'bmp']:
            paths += list(map(
                os.path.basename,
                glob.glob(self.get_data_file(f'*.{extension}'))
            ))
        for path in paths:
            with self.subTest(basename=path):
                self._test_load_image(path)


class MethodsTestCase(TestCase):
    def _test_one_method(self, filename, method, kwargs):
        method = gamera_support.methods[method]
        path = self.get_data_file(filename)
        gamera_support.init()
        in_image = gamera_support.load_image(path)
        bin_image = method(in_image, **kwargs)
        self.assertIsInstance(bin_image, gamera_support.Image)
        self.assertEqual(bin_image.data.pixel_type, gamera_support.ONEBIT)
        self.assertEqual(in_image.dim, bin_image.dim)

    def _test_methods(self, filename):
        for method in gamera_support.methods:
            with self.subTest(method=method):
                kwargs = dict()
                if method == 'global':
                    kwargs = dict(threshold=42)
                self._test_one_method(filename=filename, method=method, kwargs=kwargs)

    def test_color(self):
        self._test_methods('ycbcr-jpeg.tiff')

    def test_grey(self):
        self._test_methods('greyscale-packbits.tiff')


class ToPilRgbTestCase(TestCase):
    def _test(self, filename):
        path = self.get_data_file(filename)
        in_image = Image.open(path)
        self.addCleanup(in_image.close)
        if in_image.mode != 'RGB':
            in_image = in_image.convert('RGB')
        self.assertEqual(in_image.mode, 'RGB')
        gamera_support.init()
        gamera_image = gamera_support.load_image(path)
        out_image = gamera_support.to_pil_rgb(gamera_image)
        self.assert_images_equal(in_image, out_image)

    def test_color(self):
        self._test('ycbcr-jpeg.tiff')

    def test_grey(self):
        self._test('greyscale-packbits.tiff')


class ToPil1bppTestCase(TestCase):
    def _test(self, filename):
        path = self.get_data_file(filename)
        in_image = Image.open(path)
        self.addCleanup(in_image.close)
        if in_image.mode != '1':
            in_image = in_image.convert('1')
        self.assertEqual(in_image.mode, '1')
        gamera_support.init()
        gamera_image = gamera_support.load_image(path)
        out_image = gamera_support.to_pil_1bpp(gamera_image)
        out_image = out_image.convert('1')  # FIXME?
        self.assert_images_equal(in_image, out_image)

    def test_grey(self):
        self._test('greyscale-packbits.tiff')

    def test_mono(self):
        self._test('onebit.png')

# vim:ts=4 sts=4 sw=4 et
