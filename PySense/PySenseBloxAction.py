class BloxAction:
    """A Blox Action

    Note: All methods around Blox actions use undocumented endpoints.
    These endpoints could be modified by Sisense without notice.

    Attributes:
        json (JSON): The JSON for this object
        py_client (PySense): The connection to the Sisense server which owns this asset
    """

    def __init__(self, py_client, json):
        """

        Args:
            py_client (PySense): The PySense object for the server this asset belongs to
            json (JSON): The json for this object
        """

        self.json = json
        self.py_client = py_client

    def get_type(self):
        """Returns the type of the action (it's display name in Blox)"""

        return self.json['type']

    def get_body(self):
        """Returns the body (the actual JS) of the custom action"""

        return self.json['body']

    def get_title(self):
        """Returns the title of the action (the default button text)"""

        return self.json['snippet']['title']


