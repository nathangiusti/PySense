**Disclaimer**

1. This is not in anyway supported by Sisense. This is a hobby project of mine. 
2. Neither myself nor Sisense offer any warranty, implied or explicit. 
3. This is a work in progress. Not all calls are currently supported. 

**Overview**

PySense is a python wrapper for the Sisense REST API. The goal of this project is to make the Sisense REST API more accessible to less technical users as well as decrease the development time needed to automate tasks with the Sisense REST API.

**How to install**

pip install PySenseSDK

**How to use**

See provided examples

**V 0.0.10 Release Notes**
- Breaking changes
	- PySense.post_user renamed to PySense.add_user for clarity
	- PySense.get_dashboards_id renamed to get_dashboard_by_id for clarity
	- PySense.get_folders_id renamed to get_folder_by_id for clarity
	- The following calls had the parameter server_address added as it is necessary for running on non-local host machines
		- get_data_source_sql
		- add_security_rule
		- get_elasticube_datasecurity
		- get_elasticube_datasecurity_by_table_column
		- delete_rule

- Additions
	- New Security Example
	- PySenseElasticube.get_model returns your cube's smodel
	- PySenseElasticube.add_default_rule, creates the default rule for a table/column in a cube

- Fixes
	- Tests were not being run properly
	- Tests were not referencing the correct version of Sisense
	- Many elasticube commands would not work if not on LocalHost
