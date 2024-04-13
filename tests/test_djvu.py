# Copyright © 2015-2024 Jakub Wilk <jwilk@jwilk.net>
# Copyright © 2022-2024 FriedrichFroebel
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

import io
import os
import shutil

from tests.tools import mock, silence_truncated_file_read_warnings, TestCase

from PIL import Image

from didjvu import djvu_support as djvu
from didjvu import ipc
from didjvu import temporary


class RequirementsTestCase(TestCase):
    # noinspection PyMethodMayBeStatic
    def test_required_binaries(self):
        djvu.require_cli()


def ddjvu(djvu_file, fmt='ppm'):
    cmdline = ['ddjvu', '-1', '-format=' + fmt]
    stdio = dict(
        stdout=ipc.PIPE,
        stderr=ipc.PIPE
    )
    if isinstance(djvu_file, str):
        djvu_path = djvu_file
        cmdline += [djvu_path]
    else:
        stdio.update(stdin=djvu_file)
    child = ipc.Subprocess(cmdline, **stdio)
    stdout, stderr = child.communicate()
    stderr = stderr.decode()
    if child.returncode != 0:
        raise RuntimeError('ddjvu failed')
    if stderr != '':
        raise RuntimeError(f'ddjvu stderr: {stderr}')
    out_file = io.BytesIO(stdout)
    return Image.open(out_file)


class BitonalToDjvuTestCase(TestCase):
    def test_bitonal_to_djvu(self):
        path = self.get_data_file('onebit.bmp')
        with Image.open(path) as in_image:
            djvu_file = djvu.bitonal_to_djvu(in_image)
            out_image = ddjvu(djvu_file, fmt='pbm')
            self.addCleanup(out_image.close)
            self.assert_images_equal(in_image, out_image)


class PhotoToDjvuTestCase(TestCase):
    def test_photo_to_djvu(self):
        path = self.get_data_file('ycbcr-jpeg.tiff')
        with silence_truncated_file_read_warnings():
            with Image.open(path) as in_image:
                in_image = in_image.convert('RGB')
                mask_image = in_image.convert('1')
                djvu_file = djvu.photo_to_djvu(in_image, mask_image=mask_image)
                out_image = ddjvu(djvu_file, fmt='ppm')
                self.addCleanup(out_image.close)
                self.assert_image_sizes_equal(in_image, out_image)


class DjvuToIw44TestCase(TestCase):
    def test_djvu_to_iw44(self):
        path = self.get_data_file('ycbcr.djvu')
        with open(path, mode='rb') as in_djvu:
            out_djvu = djvu.djvu_to_iw44(in_djvu)
            in_image = ddjvu(in_djvu, fmt='ppm')
            self.addCleanup(in_image.close)
            out_image = ddjvu(out_djvu, fmt='ppm')
            self.addCleanup(out_image.close)
            self.assert_image_sizes_equal(in_image, out_image)
            in_djvu.seek(0)
            in_data = in_djvu.read()
        out_djvu.seek(0)
        out_data = out_djvu.read()
        self.assertGreater(len(in_data), len(out_data))


class MultichunkTestCase(TestCase):
    def test_sjbz(self):
        path = self.get_data_file('onebit.bmp')
        with Image.open(path) as in_image:
            width, height = in_image.size
            sjbz_path = self.get_data_file('onebit.djvu')
            multichunk = djvu.Multichunk(width, height, 100, sjbz=sjbz_path)
            djvu_file = multichunk.save()
            out_image = ddjvu(djvu_file, fmt='pbm')
            self.addCleanup(out_image.close)
            self.assert_images_equal(in_image, out_image)

    def test_incl(self):
        path = self.get_data_file('onebit.bmp')
        with Image.open(path) as in_image:
            width, height = in_image.size
            sjbz_path = self.get_data_file('onebit.djvu')
            incl_path = self.get_data_file('shared_anno.iff')
            multichunk = djvu.Multichunk(width, height, 100, sjbz=sjbz_path, incl=incl_path)
            djvu_file = multichunk.save()
            with temporary.directory() as tmpdir:
                tmp_djvu_path = os.path.join(tmpdir, 'index.djvu')
                tmp_incl_path = os.path.join(tmpdir, 'shared_anno.iff')
                os.link(djvu_file.name, tmp_djvu_path)
                shutil.copyfile(incl_path, tmp_incl_path)
                out_image = ddjvu(tmp_djvu_path, fmt='pbm')
                self.addCleanup(out_image.close)
                self.assert_images_equal(in_image, out_image)


class ValidatePageIdTestCase(TestCase):
    def test_empty(self):
        with self.assertRaises(expected_exception=ValueError) as exception_manager:
            djvu.validate_page_id('')
        self.assertEqual(
            str(exception_manager.exception),
            'page identifier must end with the .djvu extension'
        )

    def test_bad_char(self):
        with self.assertRaises(expected_exception=ValueError) as exception_manager:
            djvu.validate_page_id('eggs/ham.djvu')
        self.assertEqual(
            str(exception_manager.exception),
            'page identifier must consist only of lowercase ASCII letters, digits, _, +, - and dot'
        )

    def test_leading_bad_char(self):
        with self.assertRaises(expected_exception=ValueError) as exception_manager:
            djvu.validate_page_id('.eggs.djvu')
        self.assertEqual(
            str(exception_manager.exception),
            'page identifier cannot start with +, - or a dot'
        )

    def test_dot_dot(self):
        with self.assertRaises(expected_exception=ValueError) as exception_manager:
            djvu.validate_page_id('eggs..djvu')
        self.assertEqual(
            str(exception_manager.exception),
            'page identifier cannot contain two consecutive dots'
        )

    def test_bad_extension(self):
        with self.assertRaises(expected_exception=ValueError) as exception_manager:
            djvu.validate_page_id('eggs.png')
        self.assertEqual(
            str(exception_manager.exception),
            'page identifier must end with the .djvu extension'
        )

    def test_ok(self):
        n = 'eggs.djvu'
        self.assertEqual(djvu.validate_page_id(n), n)


class BundleDjvuViaIndirectTestCase(TestCase):
    def test_string_versus_bytes_issue(self):
        # Simplify the test by mocking away the subprocess communication which does
        # not directly influence the error.
        outer_self = self
        self._wait_called = []

        class DummySubprocess(djvu.ipc.Subprocess):
            # noinspection PyMissingConstructor
            def __init__(self, *args, **kwargs):
                # Just creating a Subprocess instance seems to run some stuff already,
                # which finally leads to some warning from `djvmcvt`:
                #   DjVuDocument.fail_URL	file://localhost/tmp/didjvu.imd61jfy/didjvu.uli33b_2djvu
                # For this reason, the `super()` call is being omitted here.
                self.stdin = io.BytesIO()

            def wait(self, timeout=None):
                outer_self._wait_called.append(self)

        with mock.patch.object(djvu.ipc, 'Subprocess', DummySubprocess):
            djvu_path = djvu.bundle_djvu_via_indirect(
                *[self.get_data_file('onebit.png')]
            )
            self.assertTrue(os.path.exists(djvu_path.name))
            self.assertEqual(2, len(self._wait_called))
