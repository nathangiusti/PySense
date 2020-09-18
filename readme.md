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
