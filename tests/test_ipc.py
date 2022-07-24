# encoding=UTF-8

# Copyright © 2010-2017 Jakub Wilk <jwilk@jwilk.net>
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

import errno
import locale
import os
import signal

from tests.tools import interim_environ, TestCase

from lib import ipc
from lib import temporary


NON_EXISTENT_COMMAND = 'didjvu-nonexistent-command'
UTF8_LOCALE_CANDIDATES = ['C.UTF-8', 'en_US.UTF-8']


class ExceptionsTestCase(TestCase):
    def test_valid(self):
        names = ['SIGINT', 'SIGABRT', 'SIGSEGV']
        for name in names:
            with self.subTest(name=name):
                signal_id = getattr(signal, name)
                exception = ipc.CalledProcessInterrupted(signal_id, 'eggs')
                self.assertEqual(
                    str(exception),
                    f"Command 'eggs' was interrupted by signal {name}"
                )

    def test_invalid_signal_id(self):
        # signal.NSIG is guaranteed not be a correct signal number
        exception = ipc.CalledProcessInterrupted(signal.NSIG, 'eggs')
        self.assertEqual(
            str(exception),
            f"Command 'eggs' was interrupted by signal {signal.NSIG}"
        )


class WaitTestCase(TestCase):
    def test_exit_code_0(self):
        child = ipc.Subprocess(['true'])
        return_code = child.wait()
        self.assertEqual(return_code, 0)

    def test_exit_code_1(self):
        child = ipc.Subprocess(['false'])
        with self.assertRaises(expected_exception=ipc.CalledProcessError) as exception_manager:
            child.wait()
        self.assertEqual(
            str(exception_manager.exception),
            "Command 'false' returned non-zero exit status 1."
        )

    def _test_signal(self, name):
        # Any long-standing process would do.
        child = ipc.Subprocess(['cat'], stdin=ipc.PIPE)
        os.kill(child.pid, getattr(signal, name))
        with self.assertRaises(expected_exception=ipc.CalledProcessInterrupted) as exception_manager:
            child.wait()
        self.assertEqual(
            str(exception_manager.exception),
            f"Command 'cat' was interrupted by signal {name}"
        )

    def test_wait_signal(self):
        names = ['SIGINT', 'SIGABRT', 'SIGSEGV']
        for name in names:
            with self.subTest(name=name):
                self._test_signal(name)


class EnvironmentTestCase(TestCase):
    @classmethod
    def get_utf8_locale(cls):
        old_locale = locale.setlocale(locale.LC_ALL)
        try:
            for new_locale in UTF8_LOCALE_CANDIDATES:
                try:
                    locale.setlocale(locale.LC_ALL, new_locale)
                except locale.Error:
                    continue
                return new_locale
        finally:
            locale.setlocale(locale.LC_ALL, old_locale)

    def setUp(self):
        self.utf8_locale = self.get_utf8_locale()

    def test_call_without_env_parameter(self):
        with interim_environ(didjvu='42'):
            child = ipc.Subprocess(
                ['sh', '-c', 'printf $didjvu'],
                stdout=ipc.PIPE, stderr=ipc.PIPE,
            )
            stdout, stderr = child.communicate()
            self.assertEqual(stdout, b'42')
            self.assertEqual(stderr, b'')

    def test_call_with_empty_env_parameter(self):
        with interim_environ(didjvu='42'):
            child = ipc.Subprocess(
                ['sh', '-c', 'printf $didjvu'],
                stdout=ipc.PIPE, stderr=ipc.PIPE,
                env=dict(),
            )
            stdout, stderr = child.communicate()
            self.assertEqual(stdout, b'42')
            self.assertEqual(stderr, b'')

    def test_call_with_custom_env_parameter(self):
        with interim_environ(didjvu='42'):
            child = ipc.Subprocess(
                ['sh', '-c', 'printf $didjvu'],
                stdout=ipc.PIPE, stderr=ipc.PIPE,
                env=dict(didjvu='24'),
            )
            stdout, stderr = child.communicate()
            self.assertEqual(stdout, b'24')
            self.assertEqual(stderr, b'')

    def test_path(self):
        path = os.getenv('PATH')
        with temporary.directory() as tmpdir:
            command_name = temporary.name(dir=tmpdir)
            command_path = os.path.join(tmpdir, command_name)
            with open(command_path, 'wt') as file:
                print('#!/bin/sh', file=file)
                print('printf 42', file=file)
            os.chmod(command_path, 0o700)
            path = str.join(os.pathsep, [tmpdir, path])
            with interim_environ(PATH=path):
                child = ipc.Subprocess(
                    [command_name],
                    stdout=ipc.PIPE, stderr=ipc.PIPE,
                )
                stdout, stderr = child.communicate()
                self.assertEqual(stdout, b'42')
                self.assertEqual(stderr, b'')

    def _test_locale(self):
        child = ipc.Subprocess(
            ['locale'],
            stdout=ipc.PIPE, stderr=ipc.PIPE
        )
        stdout, stderr = child.communicate()
        stdout = stdout.splitlines()
        stderr = stderr.splitlines()
        self.assertEqual(stderr, [])
        data = dict(line.decode().split('=', 1) for line in stdout)
        has_lc_all = has_lc_ctype = has_lang = False
        for key, value in data.items():
            if key == 'LC_ALL':
                has_lc_all = True
                self.assertEqual(value, '')
            elif key == 'LC_CTYPE':
                has_lc_ctype = True
                if self.utf8_locale is None:
                    raise self.SkipTest(
                        f'UTF-8 locale missing '
                        f'({" or ".join(UTF8_LOCALE_CANDIDATES)})'
                    )
                self.assertEqual(value, self.utf8_locale)
            elif key == 'LANG':
                has_lang = True
                self.assertEqual(value, '')
            elif key == 'LANGUAGE':
                self.assertEqual(value, '')
            else:
                self.assertEqual(value, '"POSIX"')
        self.assertTrue(has_lc_all)
        self.assertTrue(has_lc_ctype)
        self.assertTrue(has_lang)

    def test_locale_lc_all(self):
        with interim_environ(LC_ALL=self.utf8_locale):
            self._test_locale()

    def test_locale_lc_ctype(self):
        with interim_environ(LC_ALL=None, LC_CTYPE=self.utf8_locale):
            self._test_locale()

    def test_locale_lang(self):
        with interim_environ(LC_ALL=None, LC_CTYPE=None, LANG=self.utf8_locale):
            self._test_locale()


class InitExceptionTestCase(TestCase):
    def test_init_exception(self):
        with self.assertRaises(expected_exception=OSError) as exception_manager:
            ipc.Subprocess([NON_EXISTENT_COMMAND])
        exception_message = f"[Errno {errno.ENOENT}] No such file or directory: {NON_EXISTENT_COMMAND!r}"
        self.assertEqual(str(exception_manager.exception), exception_message)


class ShellEscapeTestCase(TestCase):
    def test_no_escape(self):
        value = 'eggs'
        result = ipc.shell_escape([value])
        self.assertEqual(result, value)

    def test_escape(self):
        value = '$pam'
        result = ipc.shell_escape([value])
        self.assertEqual(result, "'$pam'")
        value = "s'pam"
        result = ipc.shell_escape([value])
        self.assertEqual(result, """'s'"'"'pam'""")

    def test_list(self):
        lst = ['$pam', 'eggs', "s'pam"]
        result = ipc.shell_escape(lst)
        self.assertEqual(result, """'$pam' eggs 's'"'"'pam'""")


class RequireTestCase(TestCase):
    # noinspection PyMethodMayBeStatic
    def test_ok(self):
        ipc.require('true', 'false')

    def test_fail(self):
        with self.assertRaises(expected_exception=OSError) as exception_manager:
            ipc.require(NON_EXISTENT_COMMAND)
        exception_message = f"[Errno {errno.ENOENT}] command not found: {NON_EXISTENT_COMMAND!r}"
        self.assertEqual(str(exception_manager.exception), exception_message)

# vim:ts=4 sts=4 sw=4 et
