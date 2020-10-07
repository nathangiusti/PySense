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

**V 0.3.2 Release Notes**

- Breaking changes
    - PySenseDataSet.get_tables now returns an array of table objects
    - py_client.import_dashboard
        - Now returns an array of dashboards 
        - Has been renamed to py_client.import_dashboards
- Additions
    - Pass in your own parameters to PySense
        - If authenticating by config file you can add additional parameters. 
        - They can be accessed via py_client.get_parameter('the parameter name')
        - You can add and modify parameters via py_client.set_parameter('parameter name', 'parameter value')
    - Additional tools for admins
        - Admins can use the admin_access optional parameter to the following methods in order to perform work on unowned dashboards. 
        - The following methods have admin_access parameters
            - dashboard.export_to_dash
            - py_client.get_dashboard_by_id
            - py_client.delete_dashboard
    - Bulk import and export dashboards
        - You can use the py_client.bulk_export_dashboards to export multiple dashboards as a single file
        - You can use the py_client.import_dashboard to import a dash file with 1 to many dashboards inside
    - Caching
        - To increase performance, results from queries for elasticubes are cached to reduce calls to the server
        - The cache can be modified via config file or py_client.set_param('CUBE_CACHE_TIMEOUT_SECONDS', [the desired cache time in seconds]) 
        - You can also pass the optional parameter flush_cache=True to py_client.get_elasticubes or get_elasticube_by_name to force a flush of the cache.
        - The default value for the cache is 60 seconds 
    - Backup and Delete dashboards script
        - See the admin_access keyword in action 
        - Allows for an admin to backup and delete a list of dashboards, include those unowned by the admin
     
- Fixes
    - Elasticube sets handled better
    - Dashboard Cube usage report now used admin to get all dashboards, not just ones owned by the account

- Known Issues
    - REST API sometimes becomes responsive on Linux builds
    
