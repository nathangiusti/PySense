import unittest

from PySense import PySense


class PySenseConnectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.py_client = PySense.authenticate_by_file('//Users//nathan.giusti//Documents//PySense//VmConfig.yaml')
        cls.connection = cls.py_client.get_connections()[0]

    def test_class(self):
        connection_json = self.connection.get_json()
        self.py_client.delete_connections(self.connection)
        connection_json = self.py_client.add_connection(connection_json).get_json()
        self.connection.update_connection(connection_json)
        self.connection.sync_connection()

    @classmethod
    def tearDownClass(cls):
        return
        

if __name__ == '__main__':
    unittest.main()
