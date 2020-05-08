"""
For each elasticube, prints how many dashboards use it as a datasource. 
Script detects primary dashboard. It is unaware of specific widgets using other cubes. 
"""

from PySense import PySense

py_client = PySense.authenticate_by_file('C:\\PySense\\PySenseConfig.yaml')

dashboards = py_client.get_dashboards()
elasticubes = py_client.get_elasticubes()

elasticube_counter_dict = {}
for elasticube in elasticubes:
    elasticube_counter_dict[elasticube.get_name()] = 0

for dashboard in dashboards:
    cube_name = None
    cube = dashboard.get_datasource() 
    if cube is not None:
        cube_name = cube.get_name()
    if cube_name is not None:
        elasticube_counter_dict[cube_name] = elasticube_counter_dict[cube_name] + 1

for key, value in elasticube_counter_dict.items():
    print('Elasticube {} used {} times'.format(key, value))
    


