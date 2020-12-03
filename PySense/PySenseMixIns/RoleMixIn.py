from PySense import PySenseException


class RoleMixIn:

    def get_role_id(self, role):
        """Get the role id for the given role name. Use the SisenseRole.Role as a parameter
        from PySense import SisenseRole

        py_client.get_role_id(SisenseRole.Role.VIEWER)
        """

        if role in self._roles:
            return self._roles[role]
        return None

    def get_role_by_id(self, role_id):
        for role in self._roles:
            if self._roles[role] == role_id:
                return role
        raise PySenseException.PySenseException('No role with id {} found'.format(role_id))
