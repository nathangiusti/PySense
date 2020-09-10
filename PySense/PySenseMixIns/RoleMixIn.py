class RoleMixIn:

    def get_role_id(self, role_name):
        """Get the role id for the given role name"""

        if role_name is None:
            return None
        for item in self._roles:
            if role_name == item['name'] or role_name == item['displayName']:
                return item['_id']
        return None

    def get_role_name(self, role_id):
        """Get the role name for the given role id"""

        for item in self._roles:
            if role_id == item['_id']:
                return item['displayName']
        return None
