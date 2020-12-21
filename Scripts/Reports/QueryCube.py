"""
Use SQL to query an elasticube and write the results to a csv file.

Set the cube_name to the title of the cube to query.
Set the query to be your SQL query.
Set the path_to_save to the place to save the report. Include a file name.
"""

from PySense import PySense

cube_name = 'My Cube Name'
query = "SELECT date, category, sum([Net Revenue]) " \
        "FROM [FACT Revenue] f " \
        "GROUP BY date, category"
path_to_save = 'path//MyQuery.csv'

py_client = PySense.authenticate_by_file('C:\\PySense\\PySenseConfig.yaml')

cube = py_client.get_elasticube_by_title(cube_name)

cube.run_sql(query, "csv", path=path_to_save)
