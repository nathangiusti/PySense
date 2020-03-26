from PySense import PySense

# Authenticate with a config file. See SampleConfig.yaml for example
pyClient = PySense.authenticate_by_file('C:\\PySense\\BDSConfig.yaml')

tables = {
    # Table name / key
    'Stores': 'R_PK'
}

cube = pyClient.get_elasticube_by_name('Retailer_Summary')
if cube is not None:
    print('cube found')
for item, value in enumerate(tables):
    query = 'SELECT {}, COUNT(*) FROM {} GROUP BY {} HAVING COUNT(*) > 1'.format(value, item, item)
    print(cube.get_data_source_sql(query, 'csv'))

print('done')