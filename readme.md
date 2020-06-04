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

**V 0.2.9 Release Notes**

Hello Everyone. 

Additional development on new features of PySense will go dark for a bit as we integrate better into the API structure. 

If you find a critical release bug, please file an issue on GitHub and a patch may be released for it. 

Thank you for your patience and support
The PySense Team

- Additions
    - Authenticate by passing in a bearer token instead of having to provide username and password either inline or via config file

- Breaking changes
    - PyClient.PyClient() constructor should no longer be used. Instead use PyClient.authenticate_by_password or PyClient.authenticate_by_token
    - PyClient.authenticate_by_file is unchanged. 
    - Authentication snippets and power points have been updated to reflect the new login procedure. 

- Fixes
    - None
	
- Known Issues
    - REST API sometimes becomes responsive on Linux builds