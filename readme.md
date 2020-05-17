**Overview**

PySense is a python wrapper for the Sisense REST API. The goal of this project is to make the Sisense REST API more accessible to less technical users as well as decrease the development time needed to automate tasks with the Sisense REST API.

[Documentation](https://htmlpreview.github.io/?https://github.com/nathangiusti/PySense/blob/master/Documentation/index.html)

**How to install**

pip install PySenseSDK

**How to use**

Download the PySense Tutorial Power Point for a hands on introduction. 
- Prerequisites:
    - Basic understanding of a programming language like java script
    - Python and a python IDE installed

See snippets folder for common usage snippets

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
    - PowerPoint tutorial uses out of date syntax. 



    
   
