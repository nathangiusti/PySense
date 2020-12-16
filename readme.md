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

**V 1.0.0 Release Notes**

- Breaking changes
    - Private variables removed
        - The py_client and json class variables have been made "public" across all objects
        - If you referenced these directly, you'll need to remove the leading underscore
        - All internal JSON for an object can be accessed through the 'json' member variable
        - *.get_json() and *.set_json() methods have been removed as you can now access the JSON directly. 
        - py_client.set_debug() removed as debug is now public and can be set directly
    - Methods renamed for consistency 
        - dashboard.get_id() -> dashboard.get_oid()
        - elasticube.get_datasecurity() -> elasticube.get_data_security()
        - elasticube.get_datasecurity_by_table_column() -> elasticube.get_data_security_by_table_column()
        - elasticube.add_security_rule() -> elasticube.add_data_security_rule()
        - elasticube.delete_rule -> elasticube.delete_data_security_rule()
    - Elasticube.get_datasecurity_for_user()
        - Renamed to Elasticube.get_data_security_for_user()
        - Now takes a PySense User instead of a user_id
        - Method does not seem to work on swagger. 
    - Shares
        - A change to the shares necessitates renaming current get_shares() to get_shares_json()
        - An additional method was added to get shares by user and group. See more below in additions
    - export_* and run_sql methods now require path
        - Exports used to have the option to get the raw data back. 
        - In order to streamline code, exports will be printed directly to file. 
        - Export methods return the path of the file allowing for easy re read and modification
    - DataModel.get_schema_json() removed.
        - The schema json is different from the datamodel JSON which PySense works on. 
        - Schemas are primarily used to migrate/backup models and so will automatically be written to disk 
        - Use export_to_smodel instead
    - Elasticube.get_model()
        - Path parameter removed. If you wish to export, use export_to_smodel
        - Get model now only returns a DataModel object
        - Method only available on Linux
    - Formula management removed
        - Formulas are unsupported by the API
        - Formulas have unpredictable behavior when used/accessed/migrated through undocumented end points
    - py_client.bulk_export_dashboards()
        - Now export_dashboards, can be used to export 1 to many dashboards
        - The Sisense API does not play well with individual dash files
        - Path is now required
    - py_client.get_datamodels now always returns an array for consistency
    - Blox Actions
        - create_blox_action adds the action to Sisense automatically
        - delete_blox_action now delete_blox_actions
            - Accepts an array of Blox Actions instead of a string action type
            - Can delete multiple blox actions with one method
    - Connections
        - Connections are only manageable in Linux
        - The windows connections api is unreliable and work differently than the linux API
        - Updates and changes to connections can be managed by working directly with the connection json
       
- Additions
    - Get_shares_user_group
        - Available for Rules, DataModels, Elasticubes, and Dashboards
        - Get a list of users/groups asset is shared with 
    - Add and delete folders from PySense
    - Password
        - Can be set as optional variable when creating user
        - Can be set after user creation with user.change_password
    - Dev readme file added for those who may wish to augment PySense

    
- Fixes
    - Comments now more conformant to standards
    - Imports reorganized
    - get_shares_json() now returns the shares portion of the JSON and not the entire JSON object
    - Test now set up and tear themselves down automatically
        - Less time for new developers to work with PySense
        - Windows elasticube must still be added manually as the API does not support elasticube manipulation through the API

- Known Issues
    - REST API sometimes becomes unresponsive on Linux builds
    - REST API sometimes fails uploading sdata files
    
