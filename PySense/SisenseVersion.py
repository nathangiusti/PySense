from enum import Enum


class Version(Enum):
    """
    The Linux and Windows API's differ significantly so we need to differentiate between the two often.
    """

    WINDOWS = 1
    LINUX = 2
