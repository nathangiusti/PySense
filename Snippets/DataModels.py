from PySense import PySense

py_client = PySense.PySense('host', 'username', 'password', 'version')

# Get a data model called PySense
data_model = py_client.get_data_models(title='PySense Dev')

# Get the data models oid
data_model.get_oid()

# Delete a data model
py_client.delete_data_model(data_model)

# Add a model from one client to a new client.
new_client = PySense.PySense('newhost', 'username', 'password', 'os')
new_client.add_data_model(data_model)

data_model_to_update = new_client.get_data_models(title='PySense Prod')
new_client.add_data_model(data_model, target_data_model=data_model_to_update)
