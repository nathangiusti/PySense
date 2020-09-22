class Folder:

    def __init__(self, py_client, folder_json):
        self._py_client = py_client
        self._folder_json = folder_json

    def get_oid(self):
        """Returns the folder's oid."""
        return self._folder_json['oid']

    def get_name(self):
        """Returns the folder's name"""
        return self._folder_json['name']
