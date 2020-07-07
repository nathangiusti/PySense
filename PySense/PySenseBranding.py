class Branding:
    def __init__(self, py_client, branding_json):
        self._branding_json = branding_json
        self._py_client = py_client

    def get_json(self):
        """Return branding JSON"""
        return self._branding_json

    def set_json(self, branding_json):
        """Set branding JSON"""
        self._branding_json = branding_json
