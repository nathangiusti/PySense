from PySense import PySense

# Export tables from an elasticube
# Currently only works for localhost
table_names = ['Dim_Dates']
py_client = PySense.authenticate_by_file('C:\\PySense\\PySenseConfig.yaml')
cube = py_client.get_elasticube_by_name('PySense')
for table in table_names:
    cube.run_sql('SELECT * FROM {}'.format(table), 'csv', path='c:\\PySense\\csvs\\{}.csv'.format(table))
