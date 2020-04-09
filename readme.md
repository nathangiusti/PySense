**Disclaimer**

1. This is not in anyway supported by Sisense. This is a hobby project of mine. 
2. Neither myself nor Sisense offer any warranty, implied or explicit. 
3. This is a work in progress. Not all calls are currently supported. 

[Documentation](https://htmlpreview.github.io/?https://github.com/nathangiusti/PySense/blob/master/Documentation/index.html)

**Overview**

PySense is a python wrapper for the Sisense REST API. The goal of this project is to make the Sisense REST API more accessible to less technical users as well as decrease the development time needed to automate tasks with the Sisense REST API.

**How to install**

pip install PySenseSDK

**How to use**

See provided examples

**V 0.1.1 Release Notes**
- Breaking changes
	- elasticube.get_data_source_sql now elasticbe.run_sql
	- elasticube.get_elasticube_datasecurity now elasticube.get_datasecurity
	- elasticube.get_elasticube_datasecurity_by_table_column now elasticube.get_datasecurity_by_table_column

- Additions
	- Get data security by user from a cube
	- Get table and column for rules

- Fixes
	- None
