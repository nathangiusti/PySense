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

Download the PySense Tutorial Power Point for a hands on introduction. 
- Prerequisites:
    - Basic understanding of a programming language like java script
    - Python and a python IDE installed

See snippets folder for common usage snippets

**Planned Future Capabilities**

- Increased control over elasticube schemas

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
    
   
