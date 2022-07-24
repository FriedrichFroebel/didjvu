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

import os

from tests.tools import TestCase

from lib import filetype


class FileTypeTestCase(TestCase):
    def test_djvu(self):
        path = self.get_data_file('ycbcr.djvu')
        file_type = filetype.check(path)
        self.assertTrue(file_type.like(filetype.Djvu))
        self.assertTrue(file_type.like(filetype.DjvuSingle))

    def test_bad(self):
        path = self.get_data_file(os.devnull)
        file_type = filetype.check(path)
        self.assertFalse(file_type.like(filetype.Djvu))
        self.assertFalse(file_type.like(filetype.DjvuSingle))

# vim:ts=4 sts=4 sw=4 et
