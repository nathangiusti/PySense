**Disclaimer**

1. This is not in anyway supported by Sisense. This is a hobby project of mine. 
2. Neither myself nor Sisense offer any warranty, implied or explicit. 
3. This is a work in progress. Not all calls are currently supported. 

**Overview**

PySense is a python wrapper for the Sisense REST API. The goal of this project is to make the Sisense REST API more accessible to less technical users as well as decrease the development time needed to automate tasks with the Sisense REST API.

**How to install**

To use Sisense in your python script, download and copy the PySense.py and PySenseConfig.py to your project and import as needed. 

**How to use**

PySense supports a subset of the Sisense REST API. 

For supported REST calls the method names should match the REST API root. For example:
* get /dashboards == get_dashboards
* get /dashboards/{id}/export/pdf == get_dashboard_export_pdf
* post /dashboards/import/bulk == post_dashboards_import_bulk

Each method has two signatures, one in which every parameter is explicitly references and another where you can pass in a dictionary of parameters. 
For example get_dashboard_export_pdf could be called with:

```
query_params = {
        'paperFormat': my_paper_format,
        'paperOrientation': my_paper_orientation,
        'layout': my_layout
    }
PySense.get_dashboard_export_pdf(my_dashboard, my_path, query_params)
```

or as
```
PySense.get_dashboard_export_pdf(my_dashboard, my_path, my_paper_format, my_paper_orientation, my_layout)
```

The keys in the dictionary should match the parameters listed in the API documentation. 