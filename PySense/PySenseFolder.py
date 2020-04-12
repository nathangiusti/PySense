class Folder:

    def __init__(self, connector, folder_json):
        self._connector = connector
        self._folder_json = folder_json

    def get_id(self):
        """
        Returns the folder's id  
          
        :return: The folder's id  
        """
        
        return self._folder_json['oid']

    def get_name(self):
        """
        Returns the folder's name  
        
        :return: The folder's name  
        """
        
        return self._folder_json['name']
