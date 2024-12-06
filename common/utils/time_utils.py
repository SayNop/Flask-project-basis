import time
from typing import Union
from datetime import datetime, date, timedelta


# all function return type：str(time_str) / int(timestamp) / datetime / date


date_format_str = '%Y-%m-%d'
time_format_str = '%Y-%m-%d %H:%M:%S'


def before_date(days: int, start_time: Union[datetime, date] = datetime.today()) -> Union[datetime, date]:
    """
    get before date
    :param days: Interval days
    :param start_time: start time datetime obj
    :return: result - The return value type is consistent with the start_time
    """
    return start_time - timedelta(days=days)


def after_date(days: int, start_time: Union[datetime, date] = datetime.today()) -> Union[datetime, date]:
    """
    get after date - generate excel
    :param days: Interval days
    :param start_time: start time datetime obj
    :return: result - The return value type is consistent with the start_time
    """
    return start_time + timedelta(days=days)


def str2datetime(time_str: str, format_str: str = time_format_str) -> datetime:
    """
    convert time_str to datetime
    :param time_str: time str
    :param format_str: time str format
    :return: datetime obj
    """
    return datetime.strptime(time_str, format_str)


def str2timestamp(date_str: str, format_str: str = time_format_str, miles: bool = False) -> int:
    """
    convert time_str to timestamp
    :param date_str:time str
    :param format_str: time str format
    :param miles: Whether to use milliseconds
    :return: Integer timestamp, non-millisecond 10 digits, millisecond 13 digits
    """
    res = time.mktime(time.strptime(date_str, format_str))
    if miles:
        res = res * 1000
    return int(res)


def datetime2str(datetime_obj: Union[datetime, date], format_str: str = time_format_str) -> str:
    """
    convert datetime/date to time_str
    :param datetime_obj: datetime obj / date obj
    :param format_str: datetime format
    :return: time_str
    """
    return datetime_obj.strftime(format_str)


def datetime2timestamp(datetime_obj: datetime, miles: bool = False) -> int:
    """
    convert datetime to timestamp
    :param datetime_obj: datetime obj
    :param miles: Whether to use milliseconds
    :return: Integer timestamp, non-millisecond 10 digits, millisecond 13 digits
    """
    res = datetime.timestamp(datetime_obj)
    if miles:
        res = res * 1000
    return int(res)


def timestamp2datetime(timestamp: int) -> datetime:
    """
    convert timestamp to datetime
    :param timestamp: 10 digits timestamp
    :return: datetime
    """
    return datetime.fromtimestamp(timestamp)


def timestamp2str(timestamp: int, format_str: str = time_format_str) -> str:
    """
    convert timestamp to str
    :param timestamp: 10 digits timestamp
    :param format_str: time str format
    :return: time str
    """
    return time.strftime(format_str, time.localtime(timestamp))
