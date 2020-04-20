import unittest

from PySense import PySense


class PySenseConnectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.py_client = PySense.authenticate_by_file('C:\\PySense\\PySenseConfig.yaml')
        cls.connection = cls.py_client.get_connections(provider='JAYDBCFederator')[0]
        cls.connection_id = cls.connection.get_id()
        cls.connection_timeout = cls.connection.get_timeout()
        cls.odbc_connection = cls.py_client.get_connections(provider='ODBC')[0]
        cls.sql_connection = cls.py_client.get_connections(provider='sql')[0]
        cls.csv_connection = cls.py_client.get_connections(provider='CSV')[0]
        cls.postgres_connection = cls.py_client.get_connections(provider='PostgreSQL')[0]
        
    def test_connection(self):
        assert self.connection.get_id() is not None
        assert self.connection.get_owner() is not None
        assert self.connection.get_connection_json() is not None
        assert self.connection.get_last_updated() is not None
        assert self.connection.get_provider() is not None
        assert self.connection.get_parameters() is not None
        assert self.connection.get_timeout() is not None
        assert self.connection.get_schema() is not None
        assert self.connection.get_protected_parameters() is not None
        new_timeout = self.connection_timeout * 2
        self.connection.set_timeout(new_timeout)
        assert self.connection.get_timeout() == new_timeout
        self.connection.sync_connection()
        new_connection = self.py_client.get_connection_by_id(self.connection.get_id())
        assert new_connection.get_timeout() == self.connection.get_timeout()
        self.connection.update_connection({'timeout': self.connection_timeout})
        assert self.connection.get_timeout() == self.connection_timeout
    
    def test_odbc_connection(self):
        assert self.odbc_connection.get_server() is not None
        assert self.odbc_connection.get_culture() is not None
        assert self.odbc_connection.is_using_direct_connection() is not None
        
    def test_file_connection(self):
        assert self.csv_connection.get_api_version() is not None
        assert self.csv_connection.get_files() is not None
        assert self.csv_connection.get_ui_params() is not None
        assert self.csv_connection.get_global_table_config_options() is not None
        assert self.csv_connection.is_created_by_user() is not None
        assert self.csv_connection.get_file_name() is not None
    
    def test_sql_connection(self):
        assert self.sql_connection.get_database() is not None
        assert self.sql_connection.is_encrypted() is not None
        assert self.sql_connection.is_using_trust_certificate() is not None
    
    def test_postgres_connection(self):
        assert self.postgres_connection.get_user_name() is not None
        assert self.postgres_connection.get_password() is not None

    @classmethod
    def tearDownClass(cls):
        connection = cls.py_client.get_connection_by_id(cls.connection_id)
        connection.set_timeout(cls.connection_timeout)
        connection.sync_connection()
        

if __name__ == '__main__':
    unittest.main()
