# encoding=UTF-8

# Copyright © 2010-2019 Jakub Wilk <jwilk@jwilk.net>
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

import gc
import sys

from tests.tools import mock, TestCase

from lib import utils


class EnhanceImportTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        # noinspection PyTypeChecker
        sys.modules['nonexistent'] = None

    def test_debian(self):
        with mock.patch.object(utils, 'debian', True):
            with self.assertRaises(expected_exception=ImportError) as exception_manager:
                try:
                    # noinspection PyUnresolvedReferences
                    import nonexistent
                except ImportError as exception:
                    utils.enhance_import_error(
                        exception,
                        'PyNonexistent',
                        'python-nonexistent',
                        'https://pynonexistent.example.net/'
                    )
                    raise
                nonexistent.f()  # quieten pyflakes
            self.assertEqual(
                str(exception_manager.exception),
                (
                    'import of nonexistent halted; None in sys.modules; '
                    'please install the python-nonexistent package'
                )
            )

    def test_debian_without_debian_package_name(self):
        with mock.patch.object(utils, 'debian', True):
            with self.assertRaises(expected_exception=ImportError) as exception_manager:
                try:
                    # noinspection PyUnresolvedReferences
                    import nonexistent
                except ImportError as exception:
                    utils.enhance_import_error(
                        exception,
                        'PyNonexistent',
                        '',
                        'https://pynonexistent.example.net/'
                    )
                    raise
                nonexistent.f()  # quieten pyflakes
            self.assertEqual(
                str(exception_manager.exception),
                (
                    'import of nonexistent halted; None in sys.modules; '
                    'please install the PyNonexistent package <https://pynonexistent.example.net/>'
                )
            )

    def test_non_debian(self):
        with mock.patch.object(utils, 'debian', False):
            with self.assertRaises(expected_exception=ImportError) as exception_manager:
                try:
                    # noinspection PyUnresolvedReferences
                    import nonexistent
                except ImportError as exception:
                    utils.enhance_import_error(
                        exception,
                        'PyNonexistent',
                        'python-nonexistent',
                        'https://pynonexistent.example.net/'
                    )
                    raise
                nonexistent.f()  # quieten pyflakes
            self.assertEqual(
                str(exception_manager.exception),
                (
                    'import of nonexistent halted; None in sys.modules; '
                    'please install the PyNonexistent package <https://pynonexistent.example.net/>'
                )
            )


class ProxyTestCase(TestCase):
    def test_proxy(self):
        class Object:
            x = 42

        def wait():
            self.assertTrue(wait.ok)
            wait.ok = False

        wait.ok = False

        class Del:
            ok = False

            def __del__(self):
                type(self).ok = False

        proxy = utils.Proxy(Object, wait, [Del()])
        wait.ok = True
        self.assertEqual(proxy.x, 42)
        self.assertFalse(wait.ok)
        proxy.x = 37
        self.assertEqual(proxy.x, 37)
        self.assertEqual(Object.x, 37)
        Del.ok = True
        del proxy
        gc.collect()
        self.assertFalse(Del.ok)

# vim:ts=4 sts=4 sw=4 et
