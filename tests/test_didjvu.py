# Copyright © 2023-2024 FriedrichFroebel
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

from tempfile import NamedTemporaryFile

from tests.tools import mock, TestCase

from didjvu.didjvu import LOGGER, Main


class MainSeparateTestCase(TestCase):
    def test_generates_output_file(self):
        source_file = self.get_data_file('greyscale-packbits.tiff')
        with NamedTemporaryFile(suffix='.djvu') as target_file, \
                mock.patch.object(LOGGER, 'info'):
            with mock.patch(
                    'sys.argv',
                    ['didjvu', 'separate', source_file, '-o', target_file.name]
            ):
                Main()
            target_file.seek(0)
            first_bytes = target_file.read(280)
            self.assertEqual(280, len(first_bytes), first_bytes)


class MainEncodeTestCase(TestCase):
    def test_generates_output_file(self):
        source_file = self.get_data_file('greyscale-packbits.tiff')
        with NamedTemporaryFile(suffix='.djvu') as target_file, \
                mock.patch.object(LOGGER, 'info'):
            with mock.patch(
                    'sys.argv',
                    ['didjvu', 'encode', source_file, '-o', target_file.name]
            ):
                Main()
            target_file.seek(0)
            first_bytes = target_file.read(340)
            self.assertEqual(340, len(first_bytes), first_bytes)
