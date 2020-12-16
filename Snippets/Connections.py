from PySense import PySense

py_client = PySense.authenticate_by_file('SampleConfig.yaml')

data_model = py_client.get_data_models(title='My Data Model')
data_set = data_model.get_data_sets()[0]
connection = data_set.get_connection()
connection.update_connection({'timeout': 300})
data_set.set_connection(connection)
