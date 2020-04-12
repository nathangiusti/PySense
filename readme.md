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

See snippets folder for common usage snippets

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
