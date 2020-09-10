import unittest

from PySense import PySense


class PySenseConnectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.py_client = PySense.authenticate_by_file('//Users//nathan.giusti//Documents//PySense//PySenseLinux.yaml')
        cls.connection = cls.py_client.get_connections()[0]
        cls.red_shift_connection = cls.py_client.get_connections(provider='RedShift')[0]
        cls.sql_server_connection = cls.py_client.get_connections(provider='sql')[0]
        #cls.snowflake_connection = cls.py_client.get_connections(provider='Snowflake')[0]
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
        
    def test_file_connection(self):
        assert self.csv_connection.get_files() is not None
    
    def test_postgres_connection(self):
        assert self.postgres_connection.get_user_name() is not None
        assert self.postgres_connection.get_password() is not None

    @classmethod
    def tearDownClass(cls):
        return
        

if __name__ == '__main__':
    unittest.main()
