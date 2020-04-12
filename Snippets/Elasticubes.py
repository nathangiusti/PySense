from PySense import PySense

py_client = PySense.PySense('host', 'username', 'password')

# Get Elasticubes
elasticubes = py_client.get_elasticubes()

# Get Elasticube by name
elasticube = py_client.get_elasticube_by_name('CubeTitle')

# Run sql against cube and save result csv
elasticube.run_sql('SELECT * FROM DIM_DATES', 'csv', path='C:\\MyBackUps\\sql_res.csv')



