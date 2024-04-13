# Copyright © 2012-2015 Jakub Wilk <jwilk@jwilk.net>
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

import datetime
import time

from tests.tools import interim_environ, TestCase

from didjvu import timestamp


class NowTestCase(TestCase):
    def test_now(self):
        result = timestamp.now()
        self.assert_rfc3339_timestamp(str(result))
        dt = result.as_datetime()
        self.assertEqual(dt.dst(), datetime.timedelta(0))
        self.assertIsNone(dt.tzname())


class TimezonesTestCase(TestCase):
    def _test_timezone(self, unix_time_in_seconds, timezone, expected):
        dt_expected = expected.replace('T', ' ').replace('Z', '+00:00')
        with interim_environ(TZ=timezone):
            time.tzset()
            result = timestamp.Timestamp(unix_time_in_seconds)
            self.assert_rfc3339_timestamp(str(result))
            self.assertEqual(str(result), expected)
            dt = result.as_datetime()
            self.assertEqual(dt.dst(), datetime.timedelta(0))
            self.assertIsNone(dt.tzname())
            self.assertEqual(str(dt), dt_expected)

    def test_timezones(self):
        samples = [
            # Winter
            (1261171514, 'UTC0', '2009-12-18T21:25:14Z'),
            (1261171514, 'HAM+4:37', '2009-12-18T16:48:14-04:37'),
            (1261171514, ':Europe/Warsaw', '2009-12-18T22:25:14+01:00'),
            (1261171514, ':America/New_York', '2009-12-18T16:25:14-05:00'),
            (1261171514, ':Asia/Kathmandu', '2009-12-19T03:10:14+05:45'),
            # Summer
            (1337075844, ':Europe/Warsaw', '2012-05-15T11:57:24+02:00'),
            # Offset changes
            (1394737792, ':Europe/Moscow', '2014-03-13T23:09:52+04:00'),  # Used to be +04:00, but it's +03:00 now
        ]

        for unix_time_in_seconds, timezone, expected in samples:
            with self.subTest(unix_time_in_seconds=unix_time_in_seconds, timezone=timezone):
                self._test_timezone(
                    unix_time_in_seconds=unix_time_in_seconds,
                    timezone=timezone,
                    expected=expected
                )
