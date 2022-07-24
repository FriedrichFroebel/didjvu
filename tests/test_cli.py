# encoding=UTF-8

# Copyright © 2015-2021 Jakub Wilk <jwilk@jwilk.net>
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

import collections
import contextlib
import io
import sys

from tests.tools import mock, TestCase

from lib import cli


class RangeIntTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.type_ = cli.range_int(37, 42, 'eggs')

    def test_less_than_minimum(self):
        with self.assertRaises(expected_exception=ValueError):
            self.type_('36')

    def test_minimum(self):
        self.assertEqual(self.type_('37'), 37)

    def test_maximum(self):
        self.assertEqual(self.type_('42'), 42)

    def test_greater_than_maximum(self):
        with self.assertRaises(expected_exception=ValueError):
            self.type_('43')

    def test_non_int(self):
        with self.assertRaises(expected_exception=ValueError):
            self.type_('')
        with self.assertRaises(expected_exception=ValueError):
            self.type_('ham')


class SliceTypeTestCase(TestCase):
    def setUp(self):
        self.type_ = cli.slice_type()
        self.type_with_max_slices_1 = cli.slice_type(max_slices=1)

    def test_non_int(self):
        with self.assertRaises(expected_exception=ValueError):
            self.type_('')
        with self.assertRaises(expected_exception=ValueError):
            self.type_('ham')

    def test_negative(self):
        with self.assertRaises(expected_exception=ValueError):
            self.type_('-42')

    def test_zero(self):
        self.assertEqual(self.type_('0'), [0])

    def test_zero_1(self):
        self.assertEqual(self.type_with_max_slices_1('0'), [0])

    def test_positive(self):
        self.assertEqual(self.type_('42'), [42])

    def test_positive_1(self):
        self.assertEqual(self.type_with_max_slices_1('42'), [42])

    def test_comma(self):
        self.assertEqual(self.type_('37,42'), [37, 42])

    def test_comma_1(self):
        with self.assertRaises(expected_exception=ValueError):
            self.type_with_max_slices_1('37,42')

    def test_comma_equal(self):
        with self.assertRaises(expected_exception=ValueError):
            self.type_('37,37')

    def test_comma_less_than(self):
        with self.assertRaises(expected_exception=ValueError):
            self.type_('42,37')

    def test_plus(self):
        self.assertEqual(self.type_('37+5'), [37, 42])

    def test_plus_1(self):
        with self.assertRaises(expected_exception=ValueError):
            self.type_with_max_slices_1('37+5')

    def test_plus_equal(self):
        with self.assertRaises(expected_exception=ValueError):
            self.type_('37+0')

    def test_plus_less_than(self):
        with self.assertRaises(expected_exception=ValueError):
            self.type_('42+-5')


class SliceRepresentationTestCase(TestCase):
    def test_representation(self):
        type_ = cli.slice_type()
        samples = [
            ([0], '0'),
            ([42], '42'),
            ([23, 37, 42], '23+14+5')
        ]

        for input_list, expected_representation in samples:
            with self.subTest(input_list=input_list):
                representation = cli.get_slice_repr(input_list)
                self.assertEqual(representation, expected_representation)
                self.assertEqual(type_(representation), input_list)


class IntactTestCase(TestCase):
    def test_intact(self):
        x = object()
        intact_x = cli.intact(x)
        self.assertIs(intact_x(), x)


class ReplaceUnderscoresTestCase(TestCase):
    def test_replace_underscores(self):
        self.assertEqual(
            cli.replace_underscores('eggs_ham_spam'),
            'eggs-ham-spam'
        )


class MockActions(object):
    def __getattr__(self, name):
        def f(options):
            return name, options
        return f


class MockMethod(object):
    def __init__(self):
        self.args = dict()


class ArgumentParserTestCase(TestCase):
    def setUp(self):
        self.methods = dict(
            abutaleb=MockMethod(),
            djvu=MockMethod(),
        )
        self.actions = MockActions()

        self.action_names = collections.OrderedDict()
        self.action_names['separate'] = 1
        self.action_names['encode'] = 1
        self.action_names['bundle'] = 1

    def test_init(self):
        cli.ArgumentParser(self.methods, 'djvu')

    def test_no_args(self):
        stdout = io.StringIO()
        with mock.patch('sys.argv', ['didjvu']), \
                contextlib.redirect_stdout(stdout):
            parser = cli.ArgumentParser(self.methods, 'djvu')
            with self.assertRaises(expected_exception=SystemExit) as exception_manager:
                parser.parse_args(dict())
            self.assertEqual(exception_manager.exception.args, (2,))

        actions = ','.join(self.action_names)
        self.assertMultiLineEqual(
            stdout.getvalue(),
            (
                f'usage: didjvu [-h] [--version] {{{actions}}} ...\n'
                'didjvu: error: too few arguments\n'
            )
        )

    def _test_action_no_args(self, action):
        stderr = io.StringIO()
        with mock.patch('sys.argv', ['didjvu', action]), \
                contextlib.redirect_stderr(stderr):
            parser = cli.ArgumentParser(self.methods, 'djvu')
            with self.assertRaises(expected_exception=SystemExit) as exception_manager:
                parser.parse_args(dict())
            self.assertEqual(exception_manager.exception.args, (2,))
        self.assertRegex(
            stderr.getvalue(),
            (
                r'(?s)\A'
                f'usage: didjvu {action} .*\n'
                f'didjvu {action}: error: the following arguments are required: .*'
                r'\Z'
            )
        )

    def test_action_no_args(self):
        actions = ['separate', 'bundle', 'encode']

        for action in actions:
            with self.subTest(action=action):
                self._test_action_no_args(action=action)

    def test_bad_action(self, action='eggs'):
        stderr = io.StringIO()
        with mock.patch('sys.argv', ['didjvu', action]), \
                contextlib.redirect_stderr(stderr):
            parser = cli.ArgumentParser(self.methods, 'djvu')
            with self.assertRaises(expected_exception=SystemExit) as exception_manager:
                parser.parse_args(dict())
            self.assertEqual(exception_manager.exception.args, (2,))
        action_values = ','.join(self.action_names)
        action_strings = ', '.join(map(repr, self.action_names))
        if sys.version_info < (3, 9):
            self.assertMultiLineEqual(
                stderr.getvalue(),
                (
                    f'usage: didjvu [-h] [--version] {{{action_values}}} ...\n'
                    f"didjvu: error: invalid choice: 'eggs' (choose from {action_strings})\n"
                )
            )
        else:
            self.assertMultiLineEqual(
                stderr.getvalue(),
                (
                    f'usage: didjvu [-h] [--version] {{{action_values}}} ...\n'
                    f"didjvu: error: argument {{{action_values}}}: invalid choice: 'eggs' (choose from {action_strings})\n"
                )
            )

    def _test_action(self, action, *args):
        stderr = io.StringIO()
        argv = ['didjvu', action]
        argv += args
        with mock.patch('sys.argv', argv), contextlib.redirect_stderr(stderr):
            parser = cli.ArgumentParser(self.methods, 'djvu')
            selected_action, options = parser.parse_args(self.actions)
        self.assertMultiLineEqual(stderr.getvalue(), '')
        self.assertEqual(selected_action, action)
        return options

    def _test_action_defaults(self, action):
        path = 'eggs.png'
        options = self._test_action(action, path)
        self.assertEqual(options.input, [path])
        self.assertEqual(options.masks, [])
        self.assertIsNone(options.output)
        if action == 'bundle':
            self.assertEqual(options.page_id_template, '{base-ext}.djvu')
        else:
            self.assertIsNone(options.output_template)
        self.assertIsNone(options.dpi)
        self.assertTrue(options.fg_bg_defaults)
        self.assertEqual(options.loss_level, 0)
        self.assertEqual(options.pages_per_dict, 1)
        self.assertIs(options.method, self.methods['djvu'])
        self.assertEqual(options.params, {})
        self.assertEqual(options.verbosity, 1)
        self.assertIs(options.xmp, False)

    def test_action_defaults(self):
        actions = ['separate', 'bundle', 'encode']

        for action in actions:
            with self.subTest(action=action):
                self._test_action_defaults(action=action)

    def _test_help(self, action=None):
        argv = ['didjvu', action, '--help']
        argv = [_f for _f in argv if _f]
        stdout = io.StringIO()
        with mock.patch('sys.argv', argv), contextlib.redirect_stdout(stdout):
            parser = cli.ArgumentParser(self.methods, 'djvu')
            with self.assertRaises(expected_exception=SystemExit) as exception_manager:
                parser.parse_args(dict())
            self.assertEqual(exception_manager.exception.args, (0,))
        self.assertGreater(len(stdout.getvalue()), 0)

    def test_help(self):
        actions = [None, 'separate', 'bundle', 'encode']

        for action in actions:
            with self.subTest(action=action):
                self._test_help(action=action)

# vim:ts=4 sts=4 sw=4 et
