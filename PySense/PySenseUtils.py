from collections.abc import Iterable


def make_iterable(obj):
    if obj is None: 
        return []
    if not isinstance(obj, Iterable):
        return [obj]
    return obj

