class Branding:
    """Branding Settings

    Attributes:
        json (JSON): The JSON for this object
        py_client (PySense): The connection to the Sisense server which owns this asset
    """

    def __init__(self, py_client, branding_json):
        """

        Args:
            py_client (PySense): The PySense object for the server this asset belongs to
            branding_json (JSON): The json for this object
        """

        self.json = branding_json
        self.py_client = py_client
