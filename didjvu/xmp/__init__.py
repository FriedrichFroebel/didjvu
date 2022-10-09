# encoding=UTF-8

# Copyright © 2012-2016 Jakub Wilk <jwilk@jwilk.net>
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
XMP support
"""

import errno
import uuid

from didjvu import timestamp
from didjvu import version


def load_backend():
    try:
        # noinspection PyUnresolvedReferences
        from didjvu.xmp import gexiv2_backend
        return gexiv2_backend, None
    except ImportError as _error:  # no coverage
        error = _error

    try:
        # noinspection PyUnresolvedReferences
        from didjvu.xmp import libxmp_backend
        return libxmp_backend, error
    except ImportError:  # no coverage
        pass

    try:
        # noinspection PyUnresolvedReferences
        from didjvu.xmp import pyexiv2_backend
        return pyexiv2_backend, error
    except ImportError:  # no coverage
        pass

    return None, error


backend, import_error = load_backend()


def gen_uuid():
    """
    Generate a UUID URN, in accordance with RFC 4122.
    """
    # https://tools.ietf.org/html/rfc4122#section-3
    return f'urn:uuid:{uuid.uuid4()}'


class Event:
    def __init__(
            self,
            action=None,
            software_agent=None,
            parameters=None,
            instance_id=None,
            changed=None,
            when=None,
    ):
        if software_agent is None:
            software_agent = version.get_software_agent()
        self._items = [
            ('action', action),
            ('softwareAgent', software_agent),
            ('parameters', parameters),
            ('instanceID', instance_id),
            ('changed', changed),
            ('when', str(when)),
        ]

    @property
    def items(self):
        return iter(self._items)


def metadata(backend_module=backend):
    class Metadata(backend_module.MetadataBase):
        def update(self, media_type, internal_properties=None):
            internal_properties = internal_properties or tuple()
            instance_id = gen_uuid()
            document_id = gen_uuid()
            now = timestamp.now()
            original_media_type = self.get('dc.format')
            # TODO: try to guess original media type
            self['dc.format'] = media_type
            if original_media_type is not None:
                event_params = f'from {original_media_type} to {media_type}'
            else:
                event_params = f'to {media_type}'
            self['xmp.ModifyDate'] = now
            self['xmp.MetadataDate'] = now
            self['xmpMM.InstanceID'] = instance_id
            try:
                self['xmpMM.OriginalDocumentID']
            except KeyError:
                try:
                    original_document_id = self['xmpMM.DocumentID']
                except KeyError:
                    pass
                else:
                    self['xmpMM.OriginalDocumentID'] = original_document_id
            self['xmpMM.DocumentID'] = document_id
            event = Event(
                action='converted',
                parameters=event_params,
                instance_id=instance_id,
                when=now,
            )
            self.append_to_history(event)
            for key, value in internal_properties:
                self[f'didjvu.{key}'] = value

        def import_(self, image_filename):
            try:
                fp = open(f'{image_filename}.xmp', 'rt')
            except (OSError, IOError) as exception:
                if exception.errno == errno.ENOENT:
                    return
                raise
            try:
                self.read(fp)
            finally:
                fp.close()

        def write(self, fp):
            fp.write(self.serialize())

    return Metadata()


__all__ = [
    'backend',
    'import_error',
    'metadata',
]

# vim:ts=4 sts=4 sw=4 et
