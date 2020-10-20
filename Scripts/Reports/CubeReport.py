"""
For each elasticube, prints how many dashboards use it as a datasource. Must be an admin to run.

Script detects primary dashboard. It is unaware of specific widgets using other cubes.

report_name: The path to save the report to, including the file name.
config_file_location: The location of the config file with your Sisense credentials.

"""

from PySense import PySense

config_file_location = '/path/SampleConfig.yaml'
report_name = "/path/CubeUsageReport.csv"

py_client = PySense.authenticate_by_file(config_file_location)

dashboards = py_client.get_dashboards_admin(dashboard_type='owner')
elasticubes = py_client.get_elasticubes()

elasticube_counter_dict = {}
for elasticube in elasticubes:
    elasticube_counter_dict[elasticube.get_title()] = 0

for dashboard in dashboards:
    cube_name = None
    cube = dashboard.get_datasource() 
    if cube is not None:
        cube_name = cube.get_title()
    if cube_name is not None:
        elasticube_counter_dict[cube_name] = elasticube_counter_dict[cube_name] + 1

with open(report_name, "w") as out_file:
    out_file.write("cube,num dashboards\n")
    for key, value in elasticube_counter_dict.items():
        out_file.write("{},{}\n".format(key, value))
    


