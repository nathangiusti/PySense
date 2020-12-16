from PySense import PySenseException


class RoleMixIn:

    def get_role_id(self, role):
        """Get the role id for the given role name. Use the SisenseRole.Role as a parameter
        from PySense import SisenseRole

        py_client.get_role_id(SisenseRole.Role.VIEWER)

        Args:
            role (Role): A role enum

        Returns:
            str: The role id for the role
        """

        if role in self.roles:
            return self.roles[role]
        return None

    def get_role_by_id(self, role_id):
        """Get role from id

        Args:
            role_id (str): The role id for the role to find

        Returns:
            Role: The role with the given role id
        """

        for role in self.roles:
            if self.roles[role] == role_id:
                return role
        raise PySenseException.PySenseException('No role with id {} found'.format(role_id))
