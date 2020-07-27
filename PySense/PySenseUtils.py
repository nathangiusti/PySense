from collections.abc import Iterable
from datetime import datetime


def format_host(host):
    """Formats host for PySense"""
    if not host.startswith('http'):
        host = 'http://' + host
    if host.endswith('/'):
        host = host[:-1]
    return host


def make_iterable(obj):
    """Makes object iterable"""
    if obj is None:
        return []
    if isinstance(obj, str):
        return [obj]
    if not isinstance(obj, Iterable):
        return [obj]
    return obj


def sisense_time_to_python(datetime_str):
    """Converts a Sisense date time to a python date time."""
    return datetime.strptime(datetime_str[: -5], '%Y-%m-%dT%H:%M:%S')
