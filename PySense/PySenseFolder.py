class Folder:

    def __init__(self, host, token, folder_json):
        self._host = host
        self._token = token
        self.folder_json = folder_json

    def get_folder_id(self):
        """
        Returns the folder's id
        :return: The folder's id
        """
        return self.folder_json['oid']

    def get_folder_name(self):
        """
        Returns the folder's name
        :return: The folder's name
        """
        return self.folder_json['name']
