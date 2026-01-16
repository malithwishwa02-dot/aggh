import ctypes
import time
from contextlib import contextmanager
from datetime import datetime, timedelta

class TemporalShift:
    def __init__(self, days=90):
        self.days = days
        self.original_time = None

    def _set_system_time(self, dt):
        # SYSTEMTIME structure for Windows API
        class SYSTEMTIME(ctypes.Structure):
            _fields_ = [
                ("wYear", ctypes.c_ushort),
                ("wMonth", ctypes.c_ushort),
                ("wDayOfWeek", ctypes.c_ushort),
                ("wDay", ctypes.c_ushort),
                ("wHour", ctypes.c_ushort),
                ("wMinute", ctypes.c_ushort),
                ("wSecond", ctypes.c_ushort),
                ("wMilliseconds", ctypes.c_ushort),
            ]
        systime = SYSTEMTIME(
            dt.year, dt.month, dt.weekday(), dt.day,
            dt.hour, dt.minute, dt.second, int(dt.microsecond / 1000)
        )
        ctypes.windll.kernel32.SetSystemTime(ctypes.byref(systime))

    def __enter__(self):
        self.original_time = datetime.utcnow()
        shifted_time = self.original_time - timedelta(days=self.days)
        self._set_system_time(shifted_time)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.original_time:
            self._set_system_time(self.original_time)
