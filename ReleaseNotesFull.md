**V 0.1.2 Release Notes**
- Breaking changes
    - None

- Additions
	- Manage your plugins! Search by name and enable and disable. See plugins example script. 

- Fixes
	- None
	
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

**V 0.1.0 Release Notes**
- Breaking changes
	- The following methods were renamed for clarity/brevity/uniformity
		- Dashboard.get_dashboard_id now Dashboard.get_id
		- Dashboard.get_dashboard_title now Dashboard.get_name
		- Dashboard.get_dashboard_shares now Dashboard.get_shares
		- Dashboard.share_dashboard_to_user now Dashboard.share_to_user
		- Dashboard.unshare_dashboard_to_user now Dashboard.unshare_to_user
		- Dashboard.get_dashboard_export_png now Dashboard.export_to_png
		- Dashboard.get_dashboard_export_dash now Dashboard.export_to_dash
		- Dashboard.get_dashboard_export_pdf now Dashboard.export_to_pdf
		- Dashboard.get_dashboard_widgets now Dashboard.get_widgets
		- Dashboard.get_dashboard_widgets_by_id now Dashboard.get_widgets_by_id
		- Dashboard.post_dashboard_widgets now Dashboard.add_widget
		- Dashboard.delete_dashboards_widgets now Dashboard.delete_widget
	- The following methods no longer return a value as the REST API provides only an empty response
		- PySense.delete_groups 
		- Dashboard.delete_widget
		- Dashboard.remove_ghost_widgets
		- Group.add_user_to_group
		- Group.delete_user_from_group
		- Rule.update_rule
	- The following methods have made the path parameter optional. You can specify a path or receive back the raw contents
		- Dashboard.export_to_png
		- Dashboard.export_to_dash
		- Dashboard.export_to_pdf
	- The following methods will now use the default server address with the option to pass an alternative instead of requiring a server address
		- Elasticube.get_data_source_sql
		- Elasticube.add_security_rule
		- Elasticube.add_default_rule
		- Elasticube.get_elasticube_datasecurity
		- Elasticube.get_elasticube_datasecurity_by_table_column
		- Elasticube.delete_rule

- Additions
	- Elasticube.get_name can now be provided an extra argument to url encode the result
	- More example files for backup dashboard script
	- Move your formulas between cubes/environments
	- Export your widgets to png

- Fixes
	- Backup Dashboard example script now correctly handles widget images

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
