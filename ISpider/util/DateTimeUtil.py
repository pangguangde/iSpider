# coding:utf8
import pytz
import time

__author__ = 'pangguangde'


timezone = pytz.timezone('Asia/Shanghai')

def parseDateStringToTimestamp(date_string):
    call_time_array = time.strptime(date_string, "%Y-%m-%d %H:%M:%S")
    return int(time.mktime(call_time_array))

def parseLocalDatetimeToUTC(local_datetime):
    return timezone.localize(local_datetime).astimezone(pytz.utc)

def parseUTCDatetimeToLocal(utc_datetime):
    return utc_datetime.astimezone(timezone)
