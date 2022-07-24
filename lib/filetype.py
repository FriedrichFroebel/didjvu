# encoding=UTF-8

# Copyright © 2010-2018 Jakub Wilk <jwilk@jwilk.net>
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

"""
Filetype detection
"""


class Generic:
    def __new__(cls, *args, **kwargs):
        raise NotImplementedError  # no coverage

    @classmethod
    def like(cls, other):
        return issubclass(cls, other)


class Djvu(Generic):
    pass


class DjvuSingle(Djvu):
    pass


def check(filename):
    cls = Generic
    with open(filename, 'rb') as file:
        header = file.read(16)
        if header.startswith(b'AT&TFORM'):
            cls = Djvu
            if header.endswith(b'DJVU'):
                cls = DjvuSingle
    return cls


__all__ = [
    'check',
    'Djvu',
    'DjvuSingle',
]

# vim:ts=4 sts=4 sw=4 et
