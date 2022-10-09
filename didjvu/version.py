# encoding=UTF-8

# Copyright © 2011-2019 Jakub Wilk <jwilk@jwilk.net>
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
didjvu version information
"""

import argparse
import sys

__version__ = '0.9.1'


def get_software_agent():
    import gamera
    result = f'didjvu {__version__}'
    result += f' (Gamera {gamera.__version__})'
    return result


class VersionAction(argparse.Action):
    """
    argparse --version action
    """

    def __init__(self, option_strings, dest=argparse.SUPPRESS):
        super(VersionAction, self).__init__(
            option_strings=option_strings,
            dest=dest,
            nargs=0,
            help="show program's version information and exit"
        )

    def __call__(self, parser, namespace, values, option_string=None):
        print(f'{parser.prog} {__version__}')
        python_version = sys.version_info
        print(f'+ Python {python_version.major}.{python_version.minor}.{python_version.micro}')

        from didjvu import gamera_support
        print(f'+ Gamera {gamera_support.gamera.__version__}')
        pil_name = 'Pillow'
        try:
            # noinspection PyUnresolvedReferences
            pil_version = gamera_support.PILImage.PILLOW_VERSION
        except AttributeError:
            try:
                # noinspection PyUnresolvedReferences
                pil_version = gamera_support.PILImage.__version__
            except AttributeError:
                pil_name = 'PIL'
                # noinspection PyUnresolvedReferences
                pil_version = gamera_support.PILImage.VERSION
        print(f'+ {pil_name} {pil_version}')
        parser.exit()


__all__ = [
    'VersionAction',
    '__version__',
    'get_software_agent',
]

# vim:ts=4 sts=4 sw=4 et
