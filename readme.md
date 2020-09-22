**Overview**

PySense is the fastest, easiest way to manage and automate your Sisense deployment. 

PySense is more than just an API wrapper. PySense handles all the complexities of the Sisense API for you so you can spend more time creating value for your customers. 

I've taken my years of experience both with implementing BI solutions myself and as a consultant managing implementations for large corporations to streamline what matters most. 

With PySense you can manage your BI implementation like a pro with barely any technical skills. 

**[Documentation](https://htmlpreview.github.io/?https://github.com/nathangiusti/PySense/blob/master/Documentation/index.html)**

**Prerequisites**

Required: 
- A basic understanding of a high level programing language (JS, Java, Python, C/C++/C#, etc)
- A basic understanding of the following programming concepts
    - Control Flows (if, for, while)
    - Objects (calling object methods)
    - Collections (arrays, lists)

Recommended:
- A basic understanding of Python 

If you lack the above but still wish to use PySense I recommend [CodeAcademy](https://www.codecademy.com/learn/learn-python-3)

**Getting Started**

You'll need to have Python 3.0+ and an IDE. Development of PySense was done with [PyCharm](https://www.jetbrains.com/pycharm/).

If you need help installing Python/PyCharm, see our [tutorial](https://github.com/nathangiusti/PySense/raw/master/Installing%20Python.pptx)

Install PySense with pip:
- pip install PySenseSDK

[Tutorial Videos](https://www.youtube.com/playlist?list=PL0xO3VH5OF2JD2KiZs_41zvKvPyebg6MW)

**V 0.3.0 Release Notes**

- Breaking changes

    - Sisense Roles are now an enum.
        - There are many different names for a role that are used internally and externally. In an attempt to control for that, Roles are now implemented as an enum in SisenseRoles.Role. 
        - To get the role from a string, you can use SisenseRole.Role.from_str()
        - To add a user with the Viewer role you would do:
            add_user('my_user@example.com', SisenseRole.Role.from_str('Viewer'))
        - This will ensure stability around roles as Sisense terminology changes.
        - PySense.get_role_name -> PySense.get_role_by_id() 
            - This method now returns a SisenseRole.Role enum instead of a string
     
    - Many methods have been renamed
        - Some Sisense componenets have ids, some have oids, some have _ids, and some have multiple. When I started I wanted to see if I could remove some of the confusion by picking a single naming structure. As Sisense and PySense have grown in complexity, that goal is no longer realistic and so methods have been renamed to match their json attributes more directly.
        - In addition some methods have been renamed for brevity, clarity, and to align with the rest of PySense.
        - The parameters and usage of these methods has not changes unless noted otherwise
        - The following have been changes
            - Dashboard.get_name -> Dashboard.get_title
            - Dashboard.get_dashboard_folder -> Dashboard.get_folder
            - Elasticube.get_name -> Elasticube.get_title
            - Elasticube.get_security_for_user -> Elasticube.get_datasecurity_for_user
            - Elasticube.get_elasticube_oid -> Elasticube.get_oid
            - Folder.get_id -> Folder.get_oid
            - Widget.get_id -> Widget.get_oid
            - Group.get_id -> Group.get_oid
            
    - Undocumented endpoints have been disabled
        - When PySense first started as more of a hacked together project, I felt it would be nice to incorporate hidden endpoints. As PySense has grown it is unsustainable to keep these end points reliable. 
        - The following methods have been modified
            - DataModel.export_to_smodel no longer works on Windows
            - Elasticube.get_model no longer works on Windows
        - To manipulate datamodels in Windows, use the CLI/Prism
        
    - Snippets have been removed as the effort required to keep them in sync with versions was not worth it
    
- Additions
    - A public training series is being created. The reference material for that will be stored in the PySense Tutorial folder.

- Fixes
    - More consistent version checking

- Known Issues
    - REST API sometimes becomes responsive on Linux builds
    - 0.3.0 has a large number of changes. If you encounter problems, feel free to create GitHub issues.
    - Scripts folder was updated, but due to the difficulty of testing the scripts, there may be syntax issues. If you find them, feel free to create a GitHub issue.
    
