class Folder:
    """A folder of dashboards

    Each folder can have 0 to many dashboards or folders inside of it

    Attributes:
        json (JSON): The JSON for this object
        py_client (PySense): The connection to the Sisense server which owns this asset
    """

    def __init__(self, py_client, folder_json):
        """

        Args:
            py_client (PySense): The PySense object for the server this asset belongs to
            folder_json (JSON): The json for this object
        """

        self.py_client = py_client
        self.json = folder_json

    def get_oid(self):
        """Returns the folder's oid."""

        return self.json['oid']

    def get_name(self):
        """Returns the folder's name"""

        return self.json['name']
