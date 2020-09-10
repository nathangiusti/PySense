from PySense import PySenseUtils


def make_connection(py_client, connection_json):
    """Returns the correct connection class for the given JSON blob."""
    if connection_json['provider'] == 'ODBC':
        return ODBCConnection(py_client, connection_json)
    elif connection_json['provider'] == 'Excel':
        return ExcelConnection(py_client, connection_json)
    elif connection_json['provider'] == 'CSV':
        return CsvConnection(py_client, connection_json)
    elif connection_json['provider'] == 'sql':
        return SqlConnection(py_client, connection_json)
    elif connection_json['provider'] == 'PostgreSQL':
        return PostgreSQLConnection(py_client, connection_json)
    else:
        return Connection(py_client, connection_json)
            
    
class Connection:
    """Generic connection class.  
    
    This is the generic connection with the provider type isn't supported.     
    Attributes common to all connectors are available here.   
    Specific fields must be accessed through the connection json.  
    """

    def __init__(self, py_client, connection_json):
        self._connection_json = connection_json
        self._py_client = py_client
        
    def get_connection_json(self):
        """Gets the connection JSON  
          
        To update the connection call this method, change the needed parameters and pass this to update_connection"""
        return self._connection_json

    def get_id(self):
        """Returns the connection id"""
        return self._connection_json['_id']
    
    def get_owner(self):
        """Returns the PySense user who owns the connection"""
        return self._py_client.get_user_by_id(self._connection_json['owner'])
    
    def get_last_updated(self):
        """Returns a python datetime of the last updated"""
        return PySenseUtils.sisense_time_to_python(self._connection_json['lastUpdated'])
        
    def get_provider(self):
        """Returns the provider as a string"""
        return self._connection_json['provider']
    
    def get_parameters(self):
        """Returns a JSON blob of parameters. Varies by connection."""
        return self._connection_json['parameters']
    
    def get_timeout(self):
        """Returns the timeout for the connection in seconds"""
        return self._connection_json['timeout']
    
    def get_schema(self):
        """Returns the name of the schema"""
        return self._connection_json['schema']
    
    def get_protected_parameters(self):
        """Returns a JSON blob of protected parameters. Varies by connection"""
        return self._connection_json['protectedParameters']

    def set_parameters(self, parameters):
        """Set the parameters. Varies by connection."""
        self._connection_json['parameters'] = parameters

    def set_timeout(self, timeout):
        """Set the timeout for the connection in seconds"""
        self._connection_json['timeout'] = timeout

    def set_schema(self, schema):
        """Set the name of the schema"""
        self._connection_json['schema'] = schema
    
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
        self.update_connection(self.get_connection_json())


class ODBCConnection(Connection):
    """The connection for ODBC.

    Has additional getters and setters for ODBC specific fields.
    """

    def __init__(self, py_client, connection_json):
        super().__init__(py_client, connection_json)


class FileConnection(Connection):
    """The generic file connection.     

    Parent class for CSV and Excel   
    Has additional getters and setters for ODBC specific fields.     
    """
    def __init__(self, py_client, connection_json):
        super().__init__(py_client, connection_json)

    def get_files(self):
        """Returns an array of file locations used by the connection"""
        return self.get_parameters()['files']

    def set_files(self, files):
        """Set the files for the connector.   
        
        Args:
            - files: An array of string file locations  
        """
        self.get_parameters()['files'] = files
      
        
class ExcelConnection(FileConnection):
    """The Excel Connection"""
    def __init__(self, py_client, connection_json):
        super().__init__(py_client, connection_json)
    
    
class CsvConnection(FileConnection):
    """The CSV Connection"""
    def __init__(self, py_client, connection_json):
        super().__init__(py_client, connection_json)


class SqlConnection(ODBCConnection):
    """The Sql Connection

    Inherits from ODBC connection with additional specific getters and setters.
    """
    def __init__(self, py_client, connection_json):
        super().__init__(py_client, connection_json)


class PostgreSQLConnection(SqlConnection):
    """The PostgreSQL Connection.  
     
     Inherits from SQLConnection but has additional PostGres specific getters and setters  
     """
    def __init__(self, py_client, connection_json):
        super().__init__(py_client, connection_json)
        
    def get_user_name(self):
        """Returns the user name for the Postgres Connector"""
        return self.get_parameters()['UserName']
        
    def get_password(self):
        """Get the password for the connector"""
        return self.get_parameters()['Password']

    def set_user_name(self, user_name):
        """Set the user name for the Postgres Connector"""
        self.get_parameters()['UserName'] = user_name

    def set_password(self, password):
        """Set the password for the connector"""
        self.get_parameters()['Password'] = password
