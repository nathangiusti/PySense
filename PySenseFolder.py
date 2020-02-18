import json


class Folder:
    host = None
    token = None
    folder_json = None

    def __init__(self, host, token, folder_json):
        self.host = host
        self.token = token
        self.folder_json = folder_json

    def get_folder_oid(self):
        return self.folder_json['oid']

    def get_folder_name(self):
        return self.folder_json['name']
