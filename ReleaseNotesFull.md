**V 1.0.5 Release Notes**

- Breaking changes
    - None

- Additions
    - Datamodel exports can now return as a string. Before these changes you could only save the model to a file.
    - Split up the import_schema function from DataModelMixIn to provide functionality to upload a schema from dictionary.
        
- Fixes
    - None
    
- Known Issues
    - REST API sometimes becomes unresponsive on Linux builds
    - REST API sometimes fails uploading sdata files

**V 1.0.4 Release Notes**

- Breaking changes
    - None

- Additions
    - Fixed issue with removing duplicates when adding shares to a dashboard
        
- Fixes
    - None
    
- Known Issues
    - REST API sometimes becomes unresponsive on Linux builds
    - REST API sometimes fails uploading sdata files
  
**V 1.0.3 Release Notes**

- Breaking changes
    - None

- Additions
    - Force dashboard republish option
        
- Fixes
    - None
    
- Known Issues
    - REST API sometimes becomes unresponsive on Linux builds
    - REST API sometimes fails uploading sdata files

**V 1.0.2 Release Notes**

- Breaking changes
    - None

- Additions
    - None
        
- Fixes
    - Additional parameters now handled correctly
    
- Known Issues
    - REST API sometimes becomes unresponsive on Linux builds
    - REST API sometimes fails uploading sdata files

**V 1.0.1 Release Notes**

- Breaking changes
    - Elasticube.get_model -> Elasticube.get_data_model
    - Elasticube.get_data_security_for_user removed as the API does not appear to work
    - PySense.delete_data_model now PySense.delete_data_models 

- Additions
    - Elasticube.get_creator returns the user who created the elasticube
    - DataModel.get_creator returns the user who created the data model
        
- Fixes
    - Testing is now more platform agnostic
        - Non platform specific tests will run against TestConfig
        - Platform specific tests will only run if specified and with a targeted config file
        - More details in updated dev_readme.md
    - Tests now more resilient against being cancelled before completed
    
- Known Issues
    - REST API sometimes becomes unresponsive on Linux builds
    - REST API sometimes fails uploading sdata files

**V 1.0.0 Release Notes**

- Breaking changes
    - Private variables removed
        - The py_client and json class variables have been made "public" across all objects
        - If you referenced these directly, you'll need to remove the leading underscore
        - All internal JSON for an object can be accessed through the 'json' member variable
        - *.get_json() and *.set_json() methods have been removed as you can now access the JSON directly. 
        - py_client.set_debug() removed as debug is now public and can be set directly
    - Methods renamed for consistency 
        - dashboard.get_id() -> dashboard.get_oid()
        - elasticube.get_datasecurity() -> elasticube.get_data_security()
        - elasticube.get_datasecurity_by_table_column() -> elasticube.get_data_security_by_table_column()
        - elasticube.add_security_rule() -> elasticube.add_data_security_rule()
        - elasticube.delete_rule -> elasticube.delete_data_security_rule()
    - Elasticube.get_datasecurity_for_user()
        - Renamed to Elasticube.get_data_security_for_user()
        - Now takes a PySense User instead of a user_id
        - Method does not seem to work on swagger. 
    - Shares
        - A change to the shares necessitates renaming current get_shares() to get_shares_json()
        - An additional method was added to get shares by user and group. See more below in additions
    - export_* and run_sql methods now require path
        - Exports used to have the option to get the raw data back. 
        - In order to streamline code, exports will be printed directly to file. 
        - Export methods return the path of the file allowing for easy re read and modification
    - DataModel.get_schema_json() removed.
        - The schema json is different from the datamodel JSON which PySense works on. 
        - Schemas are primarily used to migrate/backup models and so will automatically be written to disk 
        - Use export_to_smodel instead
    - Elasticube.get_model()
        - Path parameter removed. If you wish to export, use export_to_smodel
        - Get model now only returns a DataModel object
        - Method only available on Linux
    - Formula management removed
        - Formulas are unsupported by the API
        - Formulas have unpredictable behavior when used/accessed/migrated through undocumented end points
    - py_client.bulk_export_dashboards()
        - Now export_dashboards, can be used to export 1 to many dashboards
        - The Sisense API does not play well with individual dash files
        - Path is now required
    - py_client.get_datamodels now always returns an array for consistency
    - Blox Actions
        - create_blox_action adds the action to Sisense automatically
        - delete_blox_action now delete_blox_actions
            - Accepts an array of Blox Actions instead of a string action type
            - Can delete multiple blox actions with one method
    - Connections
        - Connections are only manageable in Linux
        - The windows connections api is unreliable and work differently than the linux API
        - Updates and changes to connections can be managed by working directly with the connection json
       
- Additions
    - Get_shares_user_group
        - Available for Rules, DataModels, Elasticubes, and Dashboards
        - Get a list of users/groups asset is shared with 
    - Add and delete folders from PySense
    - Password
        - Can be set as optional variable when creating user
        - Can be set after user creation with user.change_password
    - Dev readme file added for those who may wish to augment PySense

    
- Fixes
    - Comments now more conformant to standards
    - Imports reorganized
    - get_shares_json() now returns the shares portion of the JSON and not the entire JSON object
    - Test now set up and tear themselves down automatically
        - Less time for new developers to work with PySense
        - Windows elasticube must still be added manually as the API does not support elasticube manipulation through the API

- Known Issues
    - REST API sometimes becomes unresponsive on Linux builds
    - REST API sometimes fails uploading sdata files

**V 0.3.8 Release Notes**

- Breaking changes
    - None
    
- Additions
    - Remap table/column names in your dashboard
        - Dashboard.remap_field will update all widgets and filters in a dashboard
        - Widget.remap_field will update the widget (including widget filters)
        - DOES NOT SUPPORT DATE FIELDS (this will still need to be updated manually)
        - Functionality is in beta. Please report any issues via git
- Fixes
    - Elasticube.get_data_model now correctly verifies version

- Known Issues
    - REST API sometimes becomes unresponsive on Linux builds
    - REST API sometimes fails uploading sdata files
    
**V 0.3.7 Release Notes**

- Breaking changes
    - None
    
- Additions
    - Download and upload sdata files. 
        - py_client.import_sdata()
        - datamodel.export_to_sdata()
    - Manage your blox actions (endpoints not supported by Sisense)
        - py_client.get_blox_action()
        - py_client.add_blox_action()
        - py_client.delete_blox_action()
    - Manage UI settings
        - py_client.get_ui_settings
        - py_client.set_ui_settings
              
- Fixes
    - Cleaned up imports

- Known Issues
    - REST API sometimes becomes unresponsive on Linux builds
    - REST API sometimes fails uploading sdata files

**V 0.3.6 Release Notes**

- Breaking changes
    - get_users optional param has been modified
        - role_name is now role
        - Function accepts a Sisense.Role enum instead of a string
    
- Additions
    - Authenticate by connector
        - Pass in your own connector object, useful for testing
        - Use PySense.authenticate_by_connector()
              
- Fixes
    - None

- Known Issues
    - REST API sometimes becomes unresponsive on Linux builds
    
**V 0.3.5 Release Notes**

- Breaking changes
    - None
    
- Additions
    - Ability to manage shares of unowned dashboards as admin
    - admin_access parameter added to following functions
        - Dashboard.get_shares()
        - Dashboard.add_share()
        - Dashboard.remove_shares()
              
- Fixes
    - None

- Known Issues
    - REST API sometimes becomes unresponsive on Linux builds
    

**V 0.3.4 Release Notes**

- Breaking changes
    - None
    
- Additions
    - Get the parent model of a data set DataSet.get_parent_data_model()
    - Change the build behavior of a table Table.update_build_behavior
        
- Fixes
    - Minor documentation updates

- Known Issues
    - REST API sometimes becomes unresponsive on Linux builds

**V 0.3.3 Release Notes**

- Breaking changes
    - None
    
- Additions
    - Dashboard.get_created_date get the creation date of a dashboard
    - (Beta) Active Directory integration
        - The bulk active directory endpoint has been added. Pass in a JSON array of active directory users.
        - Response will be raw JSON response from server
        
- Fixes
    - Bug in Elasticube.run_sql() resolved
    - Documentation for Elasticube.start_build() updated with more information
    - Reports renamed and updated for clarity
    - License in set up changed to match github

- Known Issues
    - REST API sometimes becomes unresponsive on Linux builds
    
**V 0.3.2 Release Notes**

- Breaking changes
    - PySenseDataSet.get_tables now returns an array of table objects
    - py_client.import_dashboard
        - Now returns an array of dashboards 
        - Has been renamed to py_client.import_dashboards
        
- Additions
    - Pass in your own parameters to PySense
        - If authenticating by config file you can add additional parameters. 
        - They can be accessed via py_client.get_parameter('the parameter name')
        - You can add and modify parameters via py_client.set_parameter('parameter name', 'parameter value')
    - Additional tools for admins
        - Admins can use the admin_access optional parameter to the following methods in order to perform work on unowned dashboards. 
        - The following methods have admin_access parameters
            - dashboard.export_to_dash
            - py_client.get_dashboard_by_id
            - py_client.delete_dashboard
    - Bulk import and export dashboards
        - You can use the py_client.bulk_export_dashboards to export multiple dashboards as a single file
        - You can use the py_client.import_dashboard to import a dash file with 1 to many dashboards inside
    - Caching
        - To increase performance, results from queries for elasticubes are cached to reduce calls to the server
        - The cache can be modified via config file or py_client.set_param('CUBE_CACHE_TIMEOUT_SECONDS', [the desired cache time in seconds]) 
        - You can also pass the optional parameter flush_cache=True to py_client.get_elasticubes or get_elasticube_by_name to force a flush of the cache.
        - The default value for the cache is 60 seconds 
    - Backup and Delete dashboards script
        - See the admin_access keyword in action 
        - Allows for an admin to backup and delete a list of dashboards, include those unowned by the admin
     
- Fixes
    - Elasticube sets handled better
    - Dashboard Cube usage report now used admin to get all dashboards, not just ones owned by the account

- Known Issues
    - REST API sometimes becomes unresponsive on Linux builds

**V 0.3.1 Release Notes**

- Breaking changes
    - None
        
- Additions
    - Import dash files from your py_client with the import_dashboard method

- Fixes

- Known Issues
    - REST API sometimes becomes responsive on Linux builds
    - Tutorial video number 3 references an out of date version of PySense. It will be redone

**V 0.3.0 Release Notes**

- Breaking changes

    - Sisense Roles are now an enum.
        - There are many different names for a role that are used internally and externally. In an attempt to control for that, Roles are now implemented as an enum in SisenseRoles.Role. 
        - To get the role from a string, you can use SisenseRole.Role.from_str()
        - To add a user with the Viewer role you would do:
            add_user('my_user@example.com', SisenseRole.Role.from_str('Viewer'))
        - This will ensure stability around roles as Sisense terminology changes.
        - PySense.get_role_name -> PySense.get_role_by_id() 
            - This method now returns a SisenseRole.Role enum instead of a string
     
    - Many methods have been renamed
        - Some Sisense components have ids, some have oids, some have _ids, and some have multiple. When I started I wanted to see if I could remove some of the confusion by picking a single naming structure. As Sisense and PySense have grown in complexity, that goal is no longer realistic and so methods have been renamed to match their json attributes more directly.
        - In addition some methods have been renamed for brevity, clarity, and to align with the rest of PySense.
        - The parameters and usage of these methods has not changes unless noted otherwise
        - The following have been changes
            - Dashboard.get_name -> Dashboard.get_title
            - Dashboard.get_dashboard_folder -> Dashboard.get_folder
            - Elasticube.get_name -> Elasticube.get_title
            - Elasticube.get_security_for_user -> Elasticube.get_datasecurity_for_user
            - Elasticube.get_elasticube_oid -> Elasticube.get_oid
            - Folder.get_id -> Folder.get_oid
            - Widget.get_id -> Widget.get_oid
            - Group.get_id -> Group.get_oid
            
    - Undocumented endpoints have been disabled
        - When PySense first started as more of a hacked together project, I felt it would be nice to incorporate hidden endpoints. As PySense has grown it is unsustainable to keep these end points reliable. 
        - The following methods have been modified
            - DataModel.export_to_smodel no longer works on Windows
            - Elasticube.get_model no longer works on Windows
        - To manipulate datamodels in Windows, use the CLI/Prism
         
- Additions
    - A public training series is being created. The reference material for that will be stored in the PySense Tutorial folder.

- Fixes
    - More consistent version checking

- Known Issues
    - REST API sometimes becomes responsive on Linux builds
    - 0.3.0 has a large number of changes. If you encounter problems, feel free to create GitHub issues.
    - Scripts folder was updated, but due to the difficulty of testing the scripts, there may be syntax issues. If you find them, feel free to create a GitHub issue.
    
**V 0.2.20 Release Notes**

- Additions
    - Get connections specific to a datamodel
        - To update a datamodel connection, get the data model, and then the data sets. 
        - Each data set is a table, you can call get/set connection on data set to change the connection for that table
        - All of this functionality is Linux only

- Fixes
    - Connection.get_id more reliable

- Breaking changes
    - PySenseConnection.get_connection_json updated to get_json for continuity
    
- Known Issues
    - REST API sometimes becomes responsive on Linux builds
 
**V 0.2.19 Release Notes**

- Additions
    - Connections have been reworked. The part is still in beta while we await user testing. 
        - When migrating a cube/datamodel between environments, the connections strings will carry over. 
        - You'll need to query the need to query the new instance and update the newly created connections. 
        - The JSON for each connector differs so there are few helper functions. 
    - You can now trigger the publishing of dashboards
        
- Fixes
    - None
    
- Breaking changes
    - None
    
- Known Issues
    - REST API sometimes becomes responsive on Linux builds
    
**V 0.2.18 Release Notes**

- Additions
    - Dashboard class now has get owner, get last updated, and get last opened options. 
    - Cube class now has get address method to get the server address.
    - New script to show how to run a sql query against an elasticube. 
    - New script to create report on how many users have opened a dashboard recently 

- Breaking changes
    - Role.get_role_id and get_role_name will return None instead of throwing an exception if a matching value is not found.
    
- Fixes
    - Dashboard.get_shares would fail if rest API call failed. Now if the rest API fails, it will check the local JSON
    - Various bug fixes to the Cube.run_sql function
    - Version checks on functions are now done in a more systemic way
    
- Known Issues
    - REST API sometimes becomes responsive on Linux builds
    - Connections in PySense are unstable. Will be fixed in future releases. 

**V 0.2.17 Release Notes**

- Additions
    - dashboard.get_widgets supports an id field to get a specific widget
    - Create new default dashboard with create_dashboard

- Breaking changes
    - None

- Fixes
    - Fixed issue with cubes not sharing with groups properly
    
- Known Issues
    - REST API sometimes becomes responsive on Linux builds
    - Connections API will no longer be developed as there appear to be issues with the underlying service in Sisense
    
**V 0.2.16 Release Notes**

- Additions
    - Export smodel files from data model
    - New data model back up script
    - Get dashboards admin endpoint implemented
    - Import smodel files into Sisense

- Breaking changes
    - None

- Fixes
    - General stability fixes on schemas and data models
    
- Known Issues
    - REST API sometimes becomes responsive on Linux builds
    - Connections API will no longer be developed as there appear to be issues with the underlying service in Sisense

**V 0.2.15 Release Notes**

- Additions
    - Script for backing up dashboards

- Breaking changes
    - None

- Fixes
    - PySenseDashboard.get_datasource returns None instead of throwing exception when no datasource is found.
    - Data Security rules applied more uniformly
    - PySenseRule.update rule now uses empty strings instead of None for default parameters
    - PySenseUtils.make_iterable now handles strings as a discrete object and not an array in and of itself
    
- Known Issues
    - REST API sometimes becomes responsive on Linux builds

**V 0.2.13 Release Notes**

- Additions
    - None

- Breaking changes
    - None

- Fixes
    - PySense root class has been reorganized for readability and maintenance
    
- Known Issues
    - REST API sometimes becomes responsive on Linux builds

**V 0.2.12 Release Notes**

- Additions
    - Now supports white labeling. See the branding snippets for details

- Breaking changes
    - None

- Fixes
    - None
    
- Known Issues
    - REST API sometimes becomes responsive on Linux builds

**V 0.2.11 Release Notes**

- Additions
    - Manage elasticube sharing
    - Sharing dashboards also shares the source cube
    - Updated sample config

- Breaking changes
    - Dashboard.get_dashboard_folder() now returns a folder object

- Fixes
    - Some documentation errors found and fixed
    - PySense will fail more gracefully when an invalid username/password is given
    - Some issues with Elasticube.get_metadata() resolved 
 
	
- Known Issues
    - REST API sometimes becomes responsive on Linux builds

**V 0.2.9 Release Notes**

- Additions
    - Authenticate by passing in a bearer token instead of having to provide username and password either inline or via config file

- Breaking changes
    - PyClient.PyClient() constructor should no longer be used. Instead use PyClient.authenticate_by_password or PyClient.authenticate_by_token
    - PyClient.authenticate_by_file is unchanged. 
    - Authentication snippets and power points have been updated to reflect the new login procedure. 

- Fixes
    - None
	
- Known Issues
    - REST API sometimes becomes responsive on Linux builds

**V 0.2.8 Release Notes**

- Additions
    - Build, start, and stop elasticubes
    - Build data models and track their build progress
    - Get detailed information about your model like the data sets, tables, and underlying model settings (like import queries)
    - New Script: Builds all data models waiting for the previous to finish
    - New Script: Get all table information from a cube/model

- Breaking changes
    - None

- Fixes
    - Elasticube comments reformatted
    - Exceptions called correctly
	
- Known Issues
    - REST API sometimes becomes responsive on Linux builds

**V 0.2.7 Release Notes**

- Additions
    - None

- Breaking changes
    - None

- Fixes
    - Verify passed correctly to login
    - Dashboard file out of sync with pip
	
- Known Issues
    - None
    
**V 0.2.6 Release Notes**

- Additions
    - New script for moving dashboards between instances
    - New script for creating users

- Breaking changes
    - post_dashboard now add_dashboards
        - Can now accept one to many dashboards
        - Takes a dashboard object instead of raw JSON
    - Widget.get_widget_json now Widget.get_json for consistency
    - PySense.get_user_by_email will now return None instead of throwing an exception if the user is not found

- Fixes
    - Snippets authentication strings now include required version argument
	
- Known Issues
    - None
    
**V 0.2.5 Release Notes**

- Additions
    - Now with additional linux support
    - In Linux export and import models
    - Scripts folder contains migrate schemas script for migrating schemas between instances
    - DataModel snippets available for reference

- Breaking changes
    - Required attribute version (either windows or linux) needed to instantiate PySense
    - Elasticube.getModel now returns a data model object 
    
- Fixes
    - Get elasticubes no longer crashes on linux
    - Documentation formatting fixes
	
- Known Issues
    - PowerPoint tutorial uses out of date syntax. 

**V 0.2.4 Release Notes**

- Additions
    - Option to set verify SSL to false. See snippets and documentation.

- Breaking changes
    - Add default rule method removed. 
    - Add security rule now has shares as optional. To make a default rule, leave shares blank.
    - New get user report script available
    
- Fixes
    - Fixed default rule not loading correctly. 
    - Some getter methods on user were throwing exceptions. 
	
- Known Issues
    - PowerPoint tutorial uses old syntax for adding security. A note has been added.

**V 0.2.3 Release Notes**
- Updated package to automatically install required dependencies

**V 0.2.2 Release Notes**
- Additions
    - Manage your connections!
        - Get, update, add, and delete connections
        - All connections supported an extent
        - Full support for PostgreSQL, ODBC, CSV, Excel, and sql
        - See the Connections snippets for more details
    - Users
        - Get user last login
        - Get user by user id
    - Dashboard
        - Get groups and users dashboard is shared with
        - Check if widget with id exists in dashboard
    
- Breaking changes
    - PySense.delete_dashboards now takes one to many dashboards instead of a single dashboard id
    - Delete widgets now takes one to many PySense widget objects instead of widget ids
    - Dashboard.add_shares now Dashboard.add_share for clarity. Method now takes on user or group object
    - Dashboard.remove_shares now takes a list of users and/or groups
    - Dashboard.delete_dashboard now takes a dashboard object instead of a dashboard id

- Fixes
    - Documentation redone for clarity
    - Dashboard will not share to user/groups already shared to
	
- Known Issues
    - Dashboard and widget export to pdf and png may cause Sisense to throw internal server errors. 
    
**V 0.2.1 Release Notes**
- Additions
    - Get a dashboards data source

- Breaking changes
    - Get dashboards parameter parent_folder_name now parent_folder and accepts the PySense folder object. 

- Fixes
    - Delete users documentation now matches function. 
    - Some snippets updated with minor improvements.
	
- Known Issues
    - Dashboard and widget export to pdf and png may cause Sisense to throw internal server errors.
    
**V 0.2.0 Release Notes**
- Additions
	- Pass a debug flag to PySense to enable logging all rest calls
	- Save elasticube model to path
	- All exceptions thrown my PySense are PySenseExceptions for better exception handling by scripts
	- Get the users in a group and add remove users from groups with ease!

- Breaking changes
	- Example scripts removed and replaced with snippets for better clarity on using Sisense
	- PySenseFolders
		- Folder.get_folder_name now Folder.get_name for clarity
		- Folder.get_folder_id now Folder.get_id for clarity
	- PySense
		- PySense.delete_user now PySense.delete_users for clarity
		- PySense.add_user username parameter now optional (set to email by default)
		- PySense.get_elasticube_by_name returns one of None elasticubes
	- PySenseDashboards
		- Dashboard.get_dashboard_folder_id now Dashboard.get_dashboard_folder and returns a folder object instead of a folder id
		- Dashboard.move_to_folder no longer returns a value
		- Dashboard.share_to_user renamed to Dashboard.add_share for clarity
		- Dashboard.unshare_to_user renamed to Dashboard.remove_share
	- PySenseElasticube
		Elasticube.add_security_rule members now optional, default is empty array
	- PySenseGroup
		- Group.get_group_id now Group.get_id for clarity
		- Group.get_group_name now Group.get_name for clarity
	- PySenseUser
		- User.get_user_id now User.get_id


- Fixes
	- Lots of new testing for increased stability
	
- Known Issues
    - Dashboard and widget export to pdf and png may cause Sisense to throw internal server errors. 

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
