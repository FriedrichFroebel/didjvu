# encoding=UTF-8

# Copyright © 2010-2021 Jakub Wilk <jwilk@jwilk.net>
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

import contextlib
import functools
import os
from unittest import mock, SkipTest, TestCase as _TestCase

from didjvu import temporary


class TestCase(_TestCase):
    maxDiff = None
    SkipTest = SkipTest

    @functools.lru_cache(maxsize=1)
    def get_data_directory(self):
        return os.path.join(os.path.dirname(__file__), 'data')

    def get_data_file(self, name):
        return os.path.join(self.get_data_directory(), name)

    def assert_image_sizes_equal(self, image1, image2):
        self.assertEqual(image1.size, image2.size)

    def assert_images_equal(self, image1, image2):
        self.assertEqual(image1.size, image2.size)
        self.assertEqual(image1.mode, image2.mode)
        equal = list(image1.getdata()) == list(image2.getdata())
        message = None
        if not equal:
            with temporary.file(delete=False, suffix='.ppm') as file1:
                image1.save(file1.name)
            with temporary.file(delete=False, suffix='.ppm') as file2:
                image2.save(file2.name)
            message = f'images are not equal: {file1.name} != {file2.name}'
        self.assertTrue(equal, msg=message)

    def assert_rfc3339_timestamp(self, timestamp):
        self.assertRegex(
            text=timestamp,
            expected_regex=r'^\d{4}(-\d{2}){2}T\d{2}(:\d{2}){2}([+-]\d{2}:\d{2}|Z)$',
        )


@contextlib.contextmanager
def interim_environ(**override):
    keys = set(override)
    copy_keys = keys & set(os.environ)
    copy = {
        key: value
        for key, value in os.environ.items()
        if key in copy_keys
    }
    for key, value in override.items():
        if value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = value
    try:
        yield
    finally:
        for key in keys:
            os.environ.pop(key, None)
        os.environ.update(copy)


@contextlib.contextmanager
def silence_truncated_file_read_warnings():
    import warnings
    with warnings.catch_warnings():
        warnings.filterwarnings(
            action='ignore', category=UserWarning, message=r'^Truncated File Read$'
        )
        yield


__all__ = [
    'mock',
    'TestCase',
    'SkipTest',
    'interim_environ',
    'silence_truncated_file_read_warnings',
]

# vim:ts=4 sts=4 sw=4 et
