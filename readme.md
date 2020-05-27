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