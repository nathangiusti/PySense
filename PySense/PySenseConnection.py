class Connection:
    """ A datasource connection

    Each data set has a connection which defines the source of the tables in the data set.

    Attributes:
        json (JSON): The JSON for this object
        py_client (PySense): The connection to the Sisense server which owns this asset
    """

    def __init__(self, py_client, json):
        """

        Args:
            py_client (PySense): The PySense object for the server this asset belongs to
            json (JSON): The json for this object
        """
        self.json = json
        self.py_client = py_client
