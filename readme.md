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
