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
        
    def get_server(self):
        """Returns the server for the ODBC Connection"""
        return self.get_parameters()['Server']
    
    def get_culture(self):
        """Returns the culture for the ODBC connection"""
        return self.get_parameters()['culture']
    
    def is_using_direct_connection(self):
        """Returns true of direct connection otherwise false"""
        if self.get_parameters()['IsUsingDirectConnection'] == 'false':
            return False
        return True

    def set_server(self, server):
        """Set the server for the ODBC Connection"""
        self.get_parameters()['Server'] = server

    def set_culture(self, culture):
        """Set the culture for the ODBC connection"""
        self.get_parameters()['culture'] = culture

    def set_is_using_direct_connection(self, boolean):
        """Returns true of direct connection otherwise false"""
        if boolean:
            self.get_parameters()['IsUsingDirectConnection'] == 'true'
        else:
            self.get_parameters()['IsUsingDirectConnection'] == 'false'


class FileConnection(Connection):
    """The generic file connection.     

    Parent class for CSV and Excel   
    Has additional getters and setters for ODBC specific fields.     
    """
    def __init__(self, py_client, connection_json):
        super().__init__(py_client, connection_json)

    def get_api_version(self):
        """Returns the API version"""
        return self.get_parameters()['ApiVersion']

    def get_files(self):
        """Returns an array of file locations used by the connection"""
        return self.get_parameters()['files']
    
    def get_ui_params(self):
        """Returns A JSON blob of UI parameters"""
        return self._connection_json['uiParams']
    
    def get_global_table_config_options(self):
        """Returns a json blob of global table config options"""
        return self._connection_json['globalTableConfigOptions']
    
    def is_created_by_user(self):
        """Returns True if connection created by user otherwise False."""
        return self._connection_json['createdByUser']
    
    def get_file_name(self):
        """Returns the file name"""
        return self._connection_json['fileName']

    def set_api_version(self, version):
        """Sets the API version"""
        self.get_parameters()['ApiVersion'] = version

    def set_files(self, files):
        """Set the files for the connector.   
        
        Args:
            - files: An array of string file locations  
        """
        self.get_parameters()['files'] = files

    def set_ui_params(self, ui_params):
        """Set the UI parameters"""
        self._connection_json['uiParams'] = ui_params

    def set_global_table_config_options(self, config):
        """Set the global table config options"""
        self._connection_json['globalTableConfigOptions'] = config

    def set_is_created_by_user(self, boolean):
        """Set if connection created by user"""
        self._connection_json['createdByUser'] = boolean

    def set_file_name(self, file_name):
        """Sets the file name"""
        self._connection_json['fileName'] = file_name
      
        
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
    
    def get_database(self):
        """Returns the database for the SQL connection"""
        return self.get_parameters()['Database']
    
    def is_encrypted(self):
        """Returns whether or not connection is encrypted"""
        if self.get_parameters()['Encrypt'] == 'false':
            return False
        return True
    
    def is_using_trust_certificate(self):
        """Returns whether or not connection is using trust certificate"""
        if self.get_parameters()['trustServerCertificate'] == 'false':
            return False
        return True

    def set_database(self, database):
        """Set the database for the SQL connection"""
        self.get_parameters()['Database'] = database

    def set_is_encrypted(self, boolean):
        """Set whether or not connection is encrypted"""
        if boolean:
            self.get_parameters()['Encrypt'] = 'false'
        else:
            self.get_parameters()['Encrypt'] = 'true'

    def set_is_using_trust_certificate(self, boolean):
        """Sets whether or not connection is using trust certificate"""
        if boolean:
            self.get_parameters()['trustServerCertificate'] = 'false'
        else:
            self.get_parameters()['trustServerCertificate'] = 'true'
        
        
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
