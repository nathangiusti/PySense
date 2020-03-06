class Widget:

    def __init__(self, host, token, widget_json):
        self._host = host
        self._token = token
        self._widget_json = widget_json

    def get_widget_json(self):
        """
        Returns the widget's JSON
        :return: The widget's JSON
        """
        return self._widget_json

    def get_widget_id(self):
        """
        Gets the widget's id
        :return: The widget's id
        """
        return self._widget_json['oid']
