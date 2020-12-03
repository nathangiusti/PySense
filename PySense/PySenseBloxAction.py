class BloxAction:
    """A Blox Action
    Note: All methods around Blox actions use undocumented endpoints.
    These endpoints could be modified by Sisense without notice.
    """

    def __init__(self, py_client, action_json):
        self._action_json = action_json
        self._py_client = py_client

    def get_type(self):
        """Returns the type of the action (it's display name in Blox)"""
        return self._action_json['type']

    def get_body(self):
        """Returns the body (the actual JS) of the custom action"""
        return self._action_json['body']

    def get_title(self):
        """Returns the title of the action (the default button text)"""
        return self._action_json['snippet']['title']

    def get_json(self):
        """Returns the raw blox action json"""
        return self._action_json


