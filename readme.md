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

**V 0.2.4 Release Notes**

- Additions
    - Option to set verify SSL to false. See snippets and documentation.

- Breaking changes
    - Add default rule method removed. 
    - Add security rule now has shares as optional. To make a default rule, leave shares blank.
    - New get user report script available
    
- Fixes
    - Fixed default rule not loading correctly. 
    - Some getter methods on user were throwing exceptions. 
	
- Known Issues
    - PowerPoint tutorial uses old syntax for adding security. A note has been added.



    
   
