# encoding=UTF-8

# Copyright © 2012 Jakub Wilk <jwilk@jwilk.net>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 dated June, 1991.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.

'''XMP support (python-xmp-toolkit backend)'''

import libxmp

from .. import timestamp

class XmpError(RuntimeError):
    pass

class MetadataBase(object):

    from libxmp.consts import XMP_NS_DC as ns_dc
    from libxmp.consts import XMP_NS_XMP as ns_xmp
    from libxmp.consts import XMP_NS_XMP_MM as ns_xmpmm
    ns_didjvu = NotImplemented

    def __init__(self):
        backend = self._backend = libxmp.XMPMeta()
        prefix = backend.register_namespace(self.ns_didjvu, 'didjvu')
        if prefix is None:
            raise XmpError('Cannot register namespace for didjvu internal properties')

    @classmethod
    def _expand_key(cls, key):
        namespace, key = key.split('.', 1)
        namespace = getattr(cls, 'ns_' + namespace.lower())
        return namespace, key

    def get(self, key, fallback=None):
        namespace, key = self._expand_key(key)
        backend = self._backend
        result = backend.get_property(namespace, key)
        if result is None:
            result = fallback
        return result

    def __getitem__(self, key):
        result = self.get(key)
        if result is None:
            raise KeyError(key)
        return result

    def __setitem__(self, key, value):
        namespace, key = self._expand_key(key)
        backend = self._backend
        if isinstance(value, bool):
            rc = backend.set_property_bool(namespace, key, value)
        elif isinstance(value, int):
            rc = backend.set_property_int(namespace, key, value)
        elif isinstance(value, list) and len(value) == 0:
            rc = backend.set_property(namespace, key, '',
                 prop_value_is_array=True,
                 prop_array_is_ordered=True
            )
        else:
            if isinstance(value, timestamp.Timestamp):
                value = str(value)
            rc = backend.set_property(namespace, key, value)
        if rc is None:
            raise XmpError('Cannot set property')

    def add_to_history(self, event, index):
        for key, value in event.items:
            if value is None:
                continue
            self['xmpMM.History[%d]/stEvt:%s' % (index, key)] = value

    def append_to_history(self, event):
        backend = self._backend
        def count_history():
            return backend.count_array_items(self.ns_xmpmm, 'History')
        count = count_history()
        if count == 0:
            self['xmpMM.History'] = []
            assert count_history() == 0
        result = self.add_to_history(event, count + 1)
        assert count_history() == count + 1
        return result

    def serialize(self):
        backend = self._backend
        return backend.serialize_and_format(omit_packet_wrapper=True, tabchr='    ')

    def read(self, file):
        backend = self._backend
        xmp = file.read()
        backend.parse_from_str(xmp)

__all__ = ['MetadataBase']

# vim:ts=4 sw=4 et