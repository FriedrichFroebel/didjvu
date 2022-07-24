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

import io

from tests.tools import mock, TestCase

from lib import fs


class CopyFileTestCase(TestCase):
    def _test_copy_file(self, data):
        input_file = io.StringIO(data)
        output_file = io.StringIO()
        length = fs.copy_file(input_file, output_file)
        self.assertEqual(output_file.tell(), length)
        output_file.seek(0)
        result = output_file.read()
        self.assertEqual(data, result)

    def test_copy_file(self):
        data = 'eggs'
        with self.subTest(data=data):
            self._test_copy_file(data)

        data = 'eggs' + 'spam' * 42
        with self.subTest(data=data):
            with mock.patch.object(fs, '_BLOCK_SIZE', 1):
                self._test_copy_file(data)


class ReplaceExtensionTestCase(TestCase):
    def test_replace_ext(self):
        result = fs.replace_ext('eggs', 'spam')
        self.assertEqual(result, 'eggs.spam')
        result = fs.replace_ext('eggs.', 'spam')
        self.assertEqual(result, 'eggs.spam')
        result = fs.replace_ext('eggs.ham', 'spam')
        self.assertEqual(result, 'eggs.spam')

# vim:ts=4 sts=4 sw=4 et
