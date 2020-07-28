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

**V 0.2.15 Release Notes**

- Additions
    - Script for backing up dashboards

- Breaking changes
    - None

- Fixes
    - PySenseDashboard.get_datasource returns None instead of throwing exception when no datasource is found.
    - Data Security rules applied more uniformly
    - PySenseRule.update rule now uses empty strings instead of None for default parameters
    - PySenseUtils.make_iterable now handles strings as a discrete object and not an array in and of itself
    
- Known Issues
    - REST API sometimes becomes responsive on Linux builds