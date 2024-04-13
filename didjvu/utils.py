# Copyright © 2011-2019 Jakub Wilk <jwilk@jwilk.net>
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

"""
Various helper functions
"""

import os

IS_DEBIAN = os.path.exists('/etc/debian_version')


def enhance_import_error(exception, package, debian_package, homepage):
    has_debian_package = bool(IS_DEBIAN and debian_package)
    message = str(exception)
    if has_debian_package:
        package = debian_package
    message += f'; please install the {package} package'
    if not has_debian_package:
        message += f' <{homepage}>'
    exception.msg = message


class Namespace:
    pass


class Proxy:
    def __init__(self, obj, wait_fn, temporaries):
        self._object = obj
        self._wait_fn = wait_fn
        self._temporaries = temporaries

    def __getattribute__(self, name):
        if name.startswith('_'):
            return object.__getattribute__(self, name)
        self._wait_fn()
        self._wait_fn = int
        return getattr(self._object, name)

    def __setattr__(self, name, value):
        if name.startswith('_'):
            return object.__setattr__(self, name, value)
        self._wait_fn()
        self._wait_fn = int
        return setattr(self._object, name, value)


__all__ = [
    'Namespace',
    'Proxy',
    'enhance_import_error',
]
