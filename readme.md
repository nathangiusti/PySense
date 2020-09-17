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

**V 0.2.19 Release Notes**

- Additions
    - Connections have been reworked. The part is still in beta while we await user testing. 
        - When migrating a cube/datamodel between environments, the connections strings will carry over. 
        - You'll need to query the need to query the new instance and update the newly created connections. 
        - The JSON for each connector differs so there are few helper functions. 
    - You can now trigger the publishing of dashboards
        
- Fixes
    - None
    
- Known Issues
    - REST API sometimes becomes responsive on Linux builds
