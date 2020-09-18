class Connection:
    """Generic connection class.  
    
    This is the generic connection with the provider type isn't supported.     
    Attributes common to all connectors are available here.   
    Specific fields must be accessed through the connection json.  
    """

    def __init__(self, py_client, connection_json):
        self._connection_json = connection_json
        self._py_client = py_client

    def get_id(self):
        """Returns the connection id"""
        if 'id' in self._connection_json:
            return self._connection_json['id']
        elif '_id' in self._connection_json:
            return self._connection_json['_id']
        else:
            return None
        
    def get_json(self):
        """Gets the connection JSON  
          
        To update the connection call this method, change the needed parameters and pass this to update_connection"""
        return self._connection_json
    
    def update_connection(self, patch_json):
        """Updates the connection based on the patch_json  
           
        Patch json can include which fields up update for example:    
        {'timeout': 1000, 'schema': 'prod'}    
        
        Args: 
            - patch_json: A json blob of fields to update   
        """
        conn_id = self.get_id()
        if '_id' in patch_json:
            conn_id = patch_json.pop('_id', None)
        if 'lastUpdated' in patch_json:
            patch_json.pop('lastUpdated', None)
        if 'protectedParameters' in patch_json:
            patch_json.pop('protectedParameters', None)
        resp_json = self._py_client.connector.rest_call('patch', 'api/v1/connection/{}'.format(conn_id), 
                                                        json_payload=patch_json)
        self._connection_json = resp_json
    
    def sync_connection(self):
        """Updates the server with the updated connection settings   
          
        This method syncs changes made to the connection locally to the server.   
        Call this method after multiple sets to sync.     
        Ex:  
        connection.set_timeout(100) -- Changes the value locally  
        connection.set_schema('newSchema') -- Changes the value locally  
        connection.sync_connection() -- Sends the new values back to the server  
        """
        self.update_connection(self.get_json())