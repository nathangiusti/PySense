from PySense import PySenseException


class RoleMixIn:

    def get_role_id(self, role_name):
        """Get the role id for the given role name"""
        if role_name is None:
            return None
        for item in self._roles:
            if role_name == item['name'] or role_name == item['displayName']:
                return item['_id']
        raise PySenseException.PySenseException('No role with name {} found'.format(role_name))

    def get_role_name(self, role_id):
        """Get the role name for the given role id"""

        for item in self._roles:
            if role_id == item['_id']:
                return item['displayName']
        raise PySenseException.PySenseException('No role with id {} found'.format(role_id))