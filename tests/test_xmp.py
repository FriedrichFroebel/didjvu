# encoding=UTF-8

# Copyright © 2012-2021 Jakub Wilk <jwilk@jwilk.net>
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

import importlib
import io
import logging
import os
from contextlib import contextmanager
from xml.etree import ElementTree

from tests.tools import SkipTest, TestCase

from didjvu import ipc
from didjvu import temporary
from didjvu import xmp
from didjvu.xmp import namespaces

logger = logging.getLogger(__name__)
del logging


def import_backend(name):
    mod_name = f'didjvu.xmp.{name}_backend'
    try:
        backend = importlib.import_module(mod_name)
    except ImportError as _import_error:
        import_error = _import_error

        class Backend:
            # Dummy replacement
            class MetadataBase:
                def __init__(self):
                    raise SkipTest(str(import_error))

        backend = Backend()
        backend.__name__ = mod_name

    return backend


XMP_BACKENDS = [
    import_backend(name)
    for name in [
        'gexiv2',
        'libxmp',
        'pyexiv2',
    ]
]

try:
    import libxmp
    import libxmp.consts
except ImportError as _libxmp_import_error:
    libxmp_import_error = _libxmp_import_error
    libxmp = None


class UuuidCheckMixin:
    UUID_REGEX = (
        r'\Aurn:uuid:XXXXXXXX-XXXX-4XXX-[89ab]XXX-XXXXXXXXXXXX\Z'
        .replace('X', '[0-9a-f]')
    )

    def assert_uuid_urn(self, uuid):
        # noinspection PyUnresolvedReferences
        self.assertRegex(
            text=uuid,
            expected_regex=self.UUID_REGEX,
        )


class UuidTestCase(UuuidCheckMixin, TestCase):
    def test_uuid(self):
        uuid1 = xmp.gen_uuid()
        self.assert_uuid_urn(uuid1)
        uuid2 = xmp.gen_uuid()
        self.assert_uuid_urn(uuid2)
        self.assertNotEqual(uuid1, uuid2)


class NamespacesTestCase(TestCase):
    def test_namespaces(self):
        if libxmp is None:
            raise self.SkipTest(str(libxmp_import_error))
        self.assertEqual(libxmp.consts.XMP_NS_DC, namespaces.dc)
        self.assertEqual(libxmp.consts.XMP_NS_RDF, namespaces.rdf)
        self.assertEqual(libxmp.consts.XMP_NS_TIFF, namespaces.tiff)
        self.assertEqual(libxmp.consts.XMP_NS_XMP, namespaces.xmp)
        self.assertEqual(libxmp.consts.XMP_NS_XMP_MM, namespaces.xmpmm)


class MetadataTestCase(UuuidCheckMixin, TestCase):
    @contextmanager
    def run_exiv2(self, filename, fail_ok=False):
        def read_from_subprocess():
            try:
                with ipc.Subprocess(
                        ['exiv2', '-P', 'Xkt', 'print', filename],
                        stdout=ipc.PIPE,
                        stderr=ipc.PIPE,
                ) as child:
                    for line in sorted(child.stdout):
                        yield line.decode('utf-8')
                    stderr = child.stderr.read()
                    if not fail_ok:
                        self.assertEqual(stderr.decode('utf-8'), '')
            except OSError as exception:
                raise self.SkipTest(str(exception))

        try:
            yield read_from_subprocess()
        except ipc.CalledProcessError:
            if not fail_ok:
                raise
        

    def assert_correct_software_agent(self, software_agent):
        self.assertRegex(
            text=software_agent,
            expected_regex=r'^didjvu [\d.]+( [(]Gamera [\d.]+[)])?',
        )

    def test_empty(self):
        for backend in XMP_BACKENDS:
            with temporary.file(mode='w+t') as xmp_file:
                exception = None
                try:
                    meta = xmp.metadata(backend_module=backend)
                    meta.write(xmp_file)
                    xmp_file.flush()
                    xmp_file.seek(0)
                except Exception as _exception:
                    exception = _exception

                with self.subTest(backend=backend.__name__, runner='exiv2'):
                    self._test_empty_exiv2(
                        xmp_file=xmp_file, exception=exception
                    )
                with self.subTest(backend=backend.__name__, runner='libxmp'):
                    self._test_empty_libxmp(
                        xmp_file=xmp_file, exception=exception
                    )

    def _test_empty_exiv2(self, xmp_file, exception=None):
        if exception is not None:
            raise exception
        with self.run_exiv2(xmp_file.name, fail_ok=True) as output:
            for line in output:
                self.assertEqual(line, '')

    def _test_empty_libxmp(self, xmp_file, exception=None):
        if exception is not None:
            raise exception
        if libxmp is None:
            raise self.SkipTest(str(libxmp_import_error))
        meta = libxmp.XMPMeta()
        meta.parse_from_str(xmp_file.read())
        xml_meta = meta.serialize_to_str(omit_all_formatting=True, omit_packet_wrapper=True)
        logger.debug(repr(xml_meta))
        xml_meta = io.StringIO(xml_meta)
        iterator = ElementTree.iterparse(xml_meta, events=('start', 'end'))

        def pop():
            return next(iterator)

        event, element = pop()
        self.assertEqual(event, 'start')
        self.assertEqual(element.tag, '{adobe:ns:meta/}xmpmeta')
        event, element = pop()
        self.assertEqual(event, 'start')
        self.assertEqual(element.tag, f'{{{namespaces.rdf}}}RDF')
        event, element = pop()
        self.assertEqual(event, 'start')
        self.assertEqual(element.tag, f'{{{namespaces.rdf}}}Description')
        self.assertEqual(element.attrib[f'{{{namespaces.rdf}}}about'], '')
        event, element = pop()
        self.assertEqual(event, 'end')
        event, element = pop()
        self.assertEqual(event, 'end')
        event, element = pop()
        self.assertEqual(event, 'end')
        try:
            event, element = pop()
        except StopIteration:
            event, element = None, None
        self.assertIsNone(event)

    def test_new(self):
        for backend in XMP_BACKENDS:
            with temporary.file(mode='w+t') as xmp_file:
                exception = None
                try:
                    meta = xmp.metadata(backend_module=backend)
                    meta.update(
                        media_type='image/x-test',
                        internal_properties=[
                            ('test_int', 42),
                            ('test_str', 'eggs'),
                            ('test_bool', True),
                        ]
                    )
                    meta.write(xmp_file)
                    xmp_file.flush()
                    xmp_file.seek(0)
                except Exception as _exception:
                    exception = _exception

                with self.subTest(backend=backend.__name__, runner='exiv2'):
                    self._test_new_exiv2(
                        xmp_file=xmp_file, exception=exception
                    )
                with self.subTest(backend=backend.__name__, runner='libxmp'):
                    self._test_new_libxmp(
                        xmp_file=xmp_file, exception=exception
                    )

    def _test_new_exiv2(self, xmp_file, exception=None):
        if exception is not None:
            raise exception

        with self.run_exiv2(xmp_file.name) as output:
            def pop():
                return tuple(next(output).rstrip('\n').split(None, 1))

            # Dublin Core:
            self.assertEqual(pop(), ('Xmp.dc.format', 'image/x-test'))
            # Internal properties:
            self.assertEqual(pop(), ('Xmp.didjvu.test_bool', 'True'))
            self.assertEqual(pop(), ('Xmp.didjvu.test_int', '42'))
            self.assertEqual(pop(), ('Xmp.didjvu.test_str', 'eggs'))
            # XMP:
            key, metadata_date = pop()
            self.assert_rfc3339_timestamp(metadata_date)
            self.assertEqual(key, 'Xmp.xmp.MetadataDate')
            key, modify_date = pop()
            self.assertEqual(key, 'Xmp.xmp.ModifyDate')
            self.assert_rfc3339_timestamp(modify_date)
            self.assertEqual(metadata_date, modify_date)
            # XMP Media Management:
            # - DocumentID:
            key, document_id = pop()
            self.assertEqual(key, 'Xmp.xmpMM.DocumentID')
            self.assert_uuid_urn(document_id)
            # - History:
            self.assertEqual(pop(), ('Xmp.xmpMM.History', 'type="Seq"'))
            # - History[1]:
            self.assertEqual(pop(), ('Xmp.xmpMM.History[1]', 'type="Struct"'))
            self.assertEqual(pop(), ('Xmp.xmpMM.History[1]/stEvt:action', 'converted'))
            key, event_instance_id = pop()
            self.assert_uuid_urn(event_instance_id)
            self.assertEqual(key, 'Xmp.xmpMM.History[1]/stEvt:instanceID')
            self.assertEqual(pop(), ('Xmp.xmpMM.History[1]/stEvt:parameters', 'to image/x-test'))
            key, software_agent = pop()
            self.assertEqual(key, 'Xmp.xmpMM.History[1]/stEvt:softwareAgent')
            self.assert_correct_software_agent(software_agent)
            key, event_date = pop()
            self.assertEqual((key, event_date), ('Xmp.xmpMM.History[1]/stEvt:when', modify_date))
            # - InstanceID:
            key, instance_id = pop()
            self.assertEqual(key, 'Xmp.xmpMM.InstanceID')
            self.assert_uuid_urn(instance_id)
            self.assertEqual(instance_id, event_instance_id)
            try:
                line = pop()
            except StopIteration:
                line = None
            self.assertIsNone(line)

    def _test_new_libxmp(self, xmp_file, exception=None):
        if exception is not None:
            raise exception
        if libxmp is None:
            raise self.SkipTest(str(libxmp_import_error))
        meta = libxmp.XMPMeta()

        def get(namespace, key):
            return meta.get_property(namespace, key)

        meta.parse_from_str(xmp_file.read())
        self.assertEqual(get(namespaces.dc, 'format'), 'image/x-test')
        modify_date = get(namespaces.xmp, 'ModifyDate')
        metadata_date = get(namespaces.xmp, 'MetadataDate')
        self.assertEqual(modify_date, metadata_date)
        document_id = get(namespaces.xmpmm, 'DocumentID')
        self.assert_uuid_urn(document_id)
        instance_id = get(namespaces.xmpmm, 'InstanceID')
        self.assert_uuid_urn(instance_id)
        self.assertEqual(get(namespaces.xmpmm, 'History[1]/stEvt:action'), 'converted')
        software_agent = get(namespaces.xmpmm, 'History[1]/stEvt:softwareAgent')
        self.assert_correct_software_agent(software_agent)
        self.assertEqual(get(namespaces.xmpmm, 'History[1]/stEvt:parameters'), 'to image/x-test')
        self.assertEqual(get(namespaces.xmpmm, 'History[1]/stEvt:instanceID'), instance_id)
        self.assertEqual(get(namespaces.xmpmm, 'History[1]/stEvt:when'), str(modify_date))
        self.assertEqual(get(namespaces.didjvu, 'test_int'), '42')
        self.assertEqual(get(namespaces.didjvu, 'test_str'), 'eggs')
        self.assertEqual(get(namespaces.didjvu, 'test_bool'), 'True')

    def test_updated(self):
        image_path = self.get_data_file('example.png')
        for backend in XMP_BACKENDS:
            with temporary.file(mode='w+t') as xmp_file:
                exception = None
                try:
                    meta = xmp.metadata(backend_module=backend)
                    meta.import_(image_path)
                    meta.update(
                        media_type='image/x-test',
                        internal_properties=[
                            ('test_int', 42),
                            ('test_str', 'eggs'),
                            ('test_bool', True),
                        ]
                    )
                    meta.write(xmp_file)
                    xmp_file.flush()
                    xmp_file.seek(0)
                except Exception as _exception:
                    exception = _exception

                with self.subTest(backend=backend.__name__, runner='exiv2'):
                    self._test_updated_exiv2(
                        xmp_file=xmp_file, exception=exception
                    )
                with self.subTest(backend=backend.__name__, runner='libxmp'):
                    self._test_updated_libxmp(
                        xmp_file=xmp_file, exception=exception
                    )

    _original_software_agent = 'scanhelper 0.6'
    _original_create_date = '2012-02-01T16:28:00+01:00'
    _original_document_id = 'urn:uuid:04fa0637-2b6e-417c-9fff-d6f0f02c08a6'
    _original_instance_id = 'urn:uuid:c3745412-65c0-4db4-880f-34fb57beddc0'

    def _test_updated_exiv2(self, xmp_file, exception=None):
        if exception is not None:
            raise exception

        with self.run_exiv2(xmp_file.name) as output:
            def pop():
                return tuple(next(output).rstrip('\n').split(None, 1))

            # Dublin Core:
            self.assertEqual(pop(), ('Xmp.dc.format', 'image/x-test'))
            # Internal properties:
            self.assertEqual(pop(), ('Xmp.didjvu.test_bool', 'True'))
            self.assertEqual(pop(), ('Xmp.didjvu.test_int', '42'))
            self.assertEqual(pop(), ('Xmp.didjvu.test_str', 'eggs'))
            # TIFF:
            self.assertEqual(pop(), ('Xmp.tiff.ImageHeight', '42'))
            self.assertEqual(pop(), ('Xmp.tiff.ImageWidth', '69'))
            # XMP:
            key, create_date = pop()
            self.assertEqual((key, create_date), ('Xmp.xmp.CreateDate', self._original_create_date))
            self.assertEqual(pop(), ('Xmp.xmp.CreatorTool', self._original_software_agent))
            key, metadata_date = pop()
            self.assertEqual(key, 'Xmp.xmp.MetadataDate')
            self.assert_rfc3339_timestamp(metadata_date)
            key, modify_date = pop()
            self.assertEqual(key, 'Xmp.xmp.ModifyDate')
            self.assert_rfc3339_timestamp(modify_date)
            self.assertEqual(metadata_date, modify_date)
            # XMP Media Management:
            # - DocumentID:
            key, document_id = pop()
            self.assertEqual(key, 'Xmp.xmpMM.DocumentID')
            self.assert_uuid_urn(document_id)
            self.assertNotEqual(document_id, self._original_document_id)
            # - History:
            self.assertEqual(pop(), ('Xmp.xmpMM.History', 'type="Seq"'))
            # - History[1]:
            self.assertEqual(pop(), ('Xmp.xmpMM.History[1]', 'type="Struct"'))
            self.assertEqual(pop(), ('Xmp.xmpMM.History[1]/stEvt:action', 'created'))
            key, original_instance_id = pop()
            self.assertEqual(key, 'Xmp.xmpMM.History[1]/stEvt:instanceID')
            self.assertEqual(original_instance_id, self._original_instance_id)
            self.assertEqual(pop(), ('Xmp.xmpMM.History[1]/stEvt:softwareAgent', self._original_software_agent))
            self.assertEqual(pop(), ('Xmp.xmpMM.History[1]/stEvt:when', create_date))
            # - History[2]:
            self.assertEqual(pop(), ('Xmp.xmpMM.History[2]', 'type="Struct"'))
            self.assertEqual(pop(), ('Xmp.xmpMM.History[2]/stEvt:action', 'converted'))
            key, event_instance_id = pop()
            self.assertEqual(key, 'Xmp.xmpMM.History[2]/stEvt:instanceID')
            self.assert_uuid_urn(event_instance_id)
            self.assertEqual(pop(), ('Xmp.xmpMM.History[2]/stEvt:parameters', 'from image/png to image/x-test'))
            key, software_agent = pop()
            self.assertEqual(key, 'Xmp.xmpMM.History[2]/stEvt:softwareAgent')
            self.assert_correct_software_agent(software_agent)
            self.assertEqual(pop(), ('Xmp.xmpMM.History[2]/stEvt:when', metadata_date))
            # - InstanceID:
            key, instance_id = pop()
            self.assertEqual(key, 'Xmp.xmpMM.InstanceID')
            self.assert_uuid_urn(instance_id)
            self.assertEqual(instance_id, event_instance_id)
            self.assertNotEqual(instance_id, original_instance_id)
            # - OriginalDocumentID:
            key, original_document_id = pop()
            self.assertEqual(key, 'Xmp.xmpMM.OriginalDocumentID')
            self.assertEqual(original_document_id, self._original_document_id)
            try:
                line = pop()
            except StopIteration:
                line = None
            self.assertIsNone(line)

    def _test_updated_libxmp(self, xmp_file, exception=None):
        if exception is not None:
            raise exception
        if libxmp is None:
            raise self.SkipTest(str(libxmp_import_error))
        meta = libxmp.XMPMeta()

        def get(namespace, key):
            return meta.get_property(namespace, key)

        meta.parse_from_str(xmp_file.read())
        self.assertEqual(get(namespaces.dc, 'format'), 'image/x-test')
        self.assertEqual(get(namespaces.tiff, 'ImageWidth'), '69')
        self.assertEqual(get(namespaces.tiff, 'ImageHeight'), '42')
        self.assertEqual(get(namespaces.xmp, 'CreatorTool'), self._original_software_agent)
        create_date = get(namespaces.xmp, 'CreateDate')
        self.assertEqual(create_date, self._original_create_date)
        modify_date = get(namespaces.xmp, 'ModifyDate')
        self.assertGreater(modify_date, create_date)
        metadata_date = get(namespaces.xmp, 'MetadataDate')
        self.assertEqual(modify_date, metadata_date)
        # (Original) DocumentID:
        original_document_id = get(namespaces.xmpmm, 'OriginalDocumentID')
        self.assertEqual(original_document_id, self._original_document_id)
        document_id = get(namespaces.xmpmm, 'DocumentID')
        self.assert_uuid_urn(document_id)
        self.assertNotEqual(document_id, original_document_id)
        self.assert_uuid_urn(document_id)
        # InstanceID:
        instance_id = get(namespaces.xmpmm, 'InstanceID')
        self.assert_uuid_urn(instance_id)
        # History[1]:
        self.assertEqual(get(namespaces.xmpmm, 'History[1]/stEvt:action'), 'created')
        self.assertEqual(get(namespaces.xmpmm, 'History[1]/stEvt:softwareAgent'), self._original_software_agent)
        original_instance_id = get(namespaces.xmpmm, 'History[1]/stEvt:instanceID')
        self.assertEqual(original_instance_id, self._original_instance_id)
        self.assertNotEqual(instance_id, original_instance_id)
        self.assertEqual(get(namespaces.xmpmm, 'History[1]/stEvt:when'), create_date)
        # History[2]:
        self.assertEqual(get(namespaces.xmpmm, 'History[2]/stEvt:action'), 'converted')
        software_agent = get(namespaces.xmpmm, 'History[2]/stEvt:softwareAgent')
        self.assert_correct_software_agent(software_agent)
        self.assertEqual(get(namespaces.xmpmm, 'History[2]/stEvt:parameters'), 'from image/png to image/x-test')
        self.assertEqual(get(namespaces.xmpmm, 'History[2]/stEvt:instanceID'), instance_id)
        self.assertEqual(get(namespaces.xmpmm, 'History[2]/stEvt:when'), modify_date)
        # Internal properties:
        self.assertEqual(get(namespaces.didjvu, 'test_int'), '42')
        self.assertEqual(get(namespaces.didjvu, 'test_str'), 'eggs')
        self.assertEqual(get(namespaces.didjvu, 'test_bool'), 'True')

    def _test_io_error(self, backend):
        image_path = self.get_data_file('nonexistent.png')
        meta = xmp.metadata(backend_module=backend)
        meta.import_(image_path)
        with temporary.directory() as tmpdir:
            os.chmod(tmpdir, 0o000)
            try:
                image_path = os.path.join(tmpdir, 'example.png')
                meta = xmp.metadata(backend_module=backend)
                with self.assertRaises(expected_exception=IOError):
                    meta.import_(image_path)
            finally:
                os.chmod(tmpdir, 0o700)

    def test_io_error(self):
        for backend in XMP_BACKENDS:
            with self.subTest(backend=backend):
                self._test_io_error(backend)

# vim:ts=4 sts=4 sw=4 et
