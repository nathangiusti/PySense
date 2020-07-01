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