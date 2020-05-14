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



    
   
