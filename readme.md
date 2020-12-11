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

**V 0.3.8 Release Notes**

- Breaking changes
    - None
    
- Additions
    - Remap table/column names in your dashboard
        - Dashboard.remap_field will update all widgets and filters in a dashboard
        - Widget.remap_field will update the widget (including widget filters)
        - DOES NOT SUPPORT DATE FIELDS (this will still need to be updated manually)
        - Functionality is in beta. Please report any issues via git
- Fixes
    - Elasticube.get_data_model now correctly verifies version

- Known Issues
    - REST API sometimes becomes unresponsive on Linux builds
    - REST API sometimes fails uploading sdata files
    
