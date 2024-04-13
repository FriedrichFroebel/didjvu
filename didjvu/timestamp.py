# Copyright © 2012-2024 Jakub Wilk <jwilk@jwilk.net>
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
Timestamps.
"""

import datetime
import time


class Timestamp:
    def __init__(self, unix_time):
        self._localtime = time.localtime(unix_time)
        datetime_current_timezone = datetime.datetime.fromtimestamp(unix_time).astimezone()
        self._timezone_delta = datetime_current_timezone.utcoffset()

    def _str(self):
        return time.strftime('%Y-%m-%dT%H:%M:%S', self._localtime)

    def _str_timezone(self):
        offset = self._timezone_delta.days * 3600 * 24 + self._timezone_delta.seconds
        if offset == 0:
            # Apparently, pyexiv2 automatically converts 00:00 offsets to “Z”.
            # Let's always use “Z” for consistency.
            return 'Z'
        hours, minutes = divmod(abs(offset) // 60, 60)
        sign = '+' if offset >= 0 else '-'
        return f'{sign}{hours:02}:{minutes:02}'

    def __str__(self):
        """
        Format the timestamp object in accordance with RFC 3339.
        """
        return self._str() + self._str_timezone()

    def as_datetime(self, cls=datetime.datetime):
        timezone_delta = self._timezone_delta

        class Timezone(datetime.tzinfo):
            def utcoffset(self, dt):
                del dt
                return timezone_delta

            def dst(self, dt):
                del dt
                return datetime.timedelta(0)

            def tzname(self, dt):
                del dt
                return

        return cls(*self._localtime[:6], tzinfo=Timezone())


def now():
    return Timestamp(time.time())


__all__ = [
    'Timestamp',
    'now'
]
