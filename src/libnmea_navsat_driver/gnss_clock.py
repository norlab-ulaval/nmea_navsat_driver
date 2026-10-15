"""GNSS time from NMEA sentences, and a feed of it to chrony.

NMEA sentences carry the UTC time of day of the fix epoch (GGA, RMC, GST,
ZDA); only RMC and ZDA also carry the date. GnssClock keeps the last date and
dates the other sentences from it, so every epoch gets a full UTC time.
"""

import calendar
import math
import socket
import struct

SECONDS_PER_DAY = 86400


class GnssClock:
    def __init__(self):
        self.ref_day = None  # days since 1970-01-01 of the last dated sentence
        self.ref_tod = None  # its UTC time of day (s)

    def update(self, parsed_sentence):
        """Return the UTC time (s since epoch) of the sentence's fix epoch, or None.

        None when the sentence has no time, or no date has been received yet.
        """
        sentence_type, data = next(iter(parsed_sentence.items()))
        tod = data.get('utc_tod', float('NaN'))
        if math.isnan(tod):
            return None

        date = None
        if sentence_type == 'RMC' and data['fix_valid']:
            date = data['date']
        elif sentence_type == 'ZDA' and data['year'] > 0:
            date = (data['year'], data['month'], data['day'])
        if date:
            self.ref_day = calendar.timegm(date + (0, 0, 0)) // SECONDS_PER_DAY
            self.ref_tod = tod
            return self.ref_day * SECONDS_PER_DAY + tod

        if self.ref_day is None:
            return None
        # A sentence without a date is from the same epoch as the last dated
        # one, or a later one: a time of day far below the reference means
        # the day rolled over at midnight in between.
        day = self.ref_day
        if tod < self.ref_tod - SECONDS_PER_DAY / 2:
            day += 1
        elif tod > self.ref_tod + SECONDS_PER_DAY / 2:
            day -= 1
        return day * SECONDS_PER_DAY + tod


class ChronySock:
    """Send (receive time, GNSS time) samples to a chrony `refclock SOCK` socket.

    The datagram is chrony's struct sock_sample (refclock_sock.c): the local
    time of the sample and the offset true time - local time.
    """
    MAGIC = 0x534f434b

    def __init__(self, path):
        self.path = path
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)

    def send(self, local_time, true_time):
        """Send one sample. Raises OSError if chronyd isn't listening."""
        sec = math.floor(local_time)
        usec = int((local_time - sec) * 1e6)
        sample = struct.pack('@qqdiiii', sec, usec, true_time - local_time,
                             0, 0, 0, self.MAGIC)
        self.sock.sendto(sample, self.path)
