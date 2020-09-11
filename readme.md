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
