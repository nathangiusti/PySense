import requests
import PySenseUtils
import PySenseConfig
import json


def get_dashboards(param_string):
    resp = requests.get('{}/api/v1/dashboards?{}'.format(PySenseConfig.host, param_string), headers=PySenseConfig.token)
    if PySenseUtils.response_successful(resp):
        return resp.json()
    return None


def get_dashboard_export_png(dashboard_id, path, param_string):
    resp = requests.get('{}/api/v1/dashboards/{}/export/png?{}'.format(PySenseConfig.host, dashboard_id, param_string),
                        headers=PySenseConfig.token)
    if PySenseUtils.response_successful(resp):
        with open(path, 'wb') as out_file:
            out_file.write(resp.content)
        return path
    return None


def get_dashboard_export_pdf(dashboard_id, path, param_string):
    resp = requests.get('{}/api/v1/dashboards/{}/export/pdf?{}'.format(PySenseConfig.host, dashboard_id, param_string),
                        headers=PySenseConfig.token)
    if PySenseUtils.response_successful(resp):
        with open(path, 'wb') as out_file:
            out_file.write(resp.content)
        return path
    return None


def post_dashboards_import_bulk(dashboard, param_string):
    dashboard = "[" + dashboard + "]"
    resp = requests.post('{}/api/v1/dashboards/import/bulk?{}'.format(PySenseConfig.host, param_string),
                         headers=PySenseConfig.token, json=json.loads(dashboard))
    return PySenseUtils.response_successful(resp)


def post_dashboard_widget_export_png(dashboard_id, widget_id, path, param_string):
    resp = requests.get('{}/api/v1/dashboards/{}/widgets/{}/export/png?{}'.format(PySenseConfig.host, dashboard_id, widget_id, param_string), headers=PySenseConfig.token)
    if PySenseUtils.response_successful(resp):
        with open(path, 'wb') as out_file:
            out_file.write(resp.content)
        return path
    else:
        return None
