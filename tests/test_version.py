# Copyright © 2015-2018 Jakub Wilk <jwilk@jwilk.net>
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

import os
import re
from xml.etree import ElementTree

from tests.tools import TestCase

from didjvu import version

_HERE = os.path.dirname(__file__)
DOC_DIRECTORY = os.path.join(_HERE, os.pardir, 'doc')


class ChangelogTestCase(TestCase):
    def test_changelog(self):
        path = os.path.join(DOC_DIRECTORY, 'changelog')
        with open(path, 'rt') as file:
            line = file.readline()
        changelog_version = line.split()[1].strip('()')
        self.assertEqual(changelog_version, version.__version__)


class ManpageTestCase(TestCase):
    def test_manpage(self):
        path = os.path.join(DOC_DIRECTORY, 'manpage.xml')
        # Do not feed path into `iterparse()` due to
        # https://github.com/python/cpython/issues/69893
        with open(path, mode='rb') as fd:
            for event, element in ElementTree.iterparse(fd):
                if element.tag == 'refmiscinfo' and element.get('class') == 'version':
                    self.assertEqual(element.text, version.__version__)
                    break
            else:
                self.fail("missing <refmiscinfo class='version'>")


class GetSoftwareAgentTestCase(TestCase):
    def test_get_software_agent(self):
        result = version.get_software_agent()
        self.assertIsInstance(result, str)
        match = re.match(r'^didjvu [\d.]+ [(]Gamera [\d.]+(pre)?[)]$', result)
        self.assertIsNotNone(match)
