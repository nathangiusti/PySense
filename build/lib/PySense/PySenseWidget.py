class Widget:

    def __init__(self, host, token, widget_json):
        self.host = host
        self.token = token
        self.widget_json = widget_json
        self.widget_id = widget_json['oid']
        self.dashboard_id = widget_json['dashboardid']

    def get_widget_id(self):
        return self.widget_id

    def get_widget_json(self):
        return self.widget_json
