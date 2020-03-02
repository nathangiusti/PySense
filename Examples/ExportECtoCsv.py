from PySense import PySense

# Export tables from a

table_names = ['Dim_Dates']
py_client = PySense.authenticate_by_file('C:\\PySense\\PySenseConfig.yaml')
cube = py_client.get_elasticube_by_name('PySense')
for table in table_names:
    cube.get_data_source_sql('c:\\PySense\\csvs\\{}.csv'.format(table), 'SELECT * FROM {}'.format(table), 'csv')
