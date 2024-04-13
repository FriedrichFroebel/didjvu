# Copyright © 2010-2015 Jakub Wilk <jwilk@jwilk.net>
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

from tests.tools import TestCase

from didjvu import templates


class TemplatesTestCase(TestCase):
    def test_name(self):
        path = '/path/to/eggs.png'
        memo = {}
        result = templates.expand('{name}', path, 0, memo)
        self.assertEqual(result, '/path/to/eggs.png')
        result = templates.expand('{base}', path, 0, memo)
        self.assertEqual(result, 'eggs.png')
        result = templates.expand('{name-ext}.djvu', path, 0, memo)
        self.assertEqual(result, '/path/to/eggs.djvu')
        result = templates.expand('{base-ext}.djvu', path, 0, memo)
        self.assertEqual(result, 'eggs.djvu')

    def test_page(self):
        path = '/path/to/eggs.png'
        memo = {}
        result = templates.expand('{page}', path, 0, memo)
        self.assertEqual(result, '1')
        result = templates.expand('{page:04}', path, 0, memo)
        self.assertEqual(result, '0001')
        result = templates.expand('{page}', path, 42, memo)
        self.assertEqual(result, '43')
        result = templates.expand('{page+26}', path, 42, memo)
        self.assertEqual(result, '69')
        result = templates.expand('{page-26}', path, 42, memo)
        self.assertEqual(result, '17')

    def test_bad_offset(self):
        path = '/path/to/eggs.png'
        with self.assertRaises(expected_exception=KeyError) as exception_manager:
            templates.expand('{page+ham}', path, 42, {})
        self.assertEqual(exception_manager.exception.args, ('page+ham',))

    def test_bad_type_offset(self):
        path = '/path/to/eggs.png'
        with self.assertRaises(expected_exception=KeyError) as exception_manager:
            templates.expand('{base-37}', path, 42, {})
        self.assertEqual(exception_manager.exception.args, ('base-37',))

    def test_bad_var_offset(self):
        path = '/path/to/eggs.png'
        with self.assertRaises(expected_exception=KeyError) as exception_manager:
            templates.expand('{eggs-37}', path, 42, {})
        self.assertEqual(exception_manager.exception.args, ('eggs-37',))

    def test_multi_offset(self):
        path = '/path/to/eggs.png'
        with self.assertRaises(expected_exception=KeyError) as exception_manager:
            templates.expand('{eggs+bacon+ham}', path, 42, {})
        self.assertEqual(exception_manager.exception.args, ('eggs+bacon+ham',))
        with self.assertRaises(expected_exception=KeyError) as exception_manager:
            templates.expand('{eggs-bacon-ham}', path, 42, {})
        self.assertEqual(exception_manager.exception.args, ('eggs-bacon-ham',))

    def test_duplicates(self):
        path = '/path/to/eggs.png'
        memo = {}
        result = templates.expand('{base-ext}.djvu', path, 0, memo)
        self.assertEqual(result, 'eggs.djvu')
        result = templates.expand('{base-ext}.djvu', path, 0, memo)
        self.assertEqual(result, 'eggs.1.djvu')
        result = templates.expand('{base-ext}.djvu', path, 0, memo)
        self.assertEqual(result, 'eggs.2.djvu')
        result = templates.expand('{base-ext}.2.djvu', path, 0, memo)
        self.assertEqual(result, 'eggs.2.1.djvu')
        result = templates.expand('{base-ext}.2.djvu', path, 0, memo)
        self.assertEqual(result, 'eggs.2.2.djvu')
