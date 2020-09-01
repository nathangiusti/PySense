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
