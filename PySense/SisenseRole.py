from enum import Enum

from PySense import PySenseException


class Role(Enum):
    """
    Enumeration of the different user roles in Sisense
    """

    DATA_DESIGNER = 'dataDesigner'
    SYS_ADMIN = 'super'
    DATA_ADMIN = 'dataAdmin'
    ADMIN = 'admin'
    DESIGNER = 'contributor'
    VIEWER = 'consumer'

    @staticmethod
    def from_str(role):
        """Returns the Role for a given string"""
        role = role.lower().replace(" ", "")
        if role in ['datadesigner', 'data_designer']:
            return Role.DATA_DESIGNER
        elif role in ['super', 'sysadmin', 'sys_admin']:
            return Role.SYS_ADMIN
        elif role in ['dataadmin', 'data_admin']:
            return Role.DATA_ADMIN
        elif role in ['admin']:
            return Role.ADMIN
        elif role in ['contributor', 'designer']:
            return Role.DESIGNER
        elif role in ['consumer', 'viewer']:
            return Role.VIEWER
        else:
            raise PySenseException.PySenseException('No such role {} found'.format(role))