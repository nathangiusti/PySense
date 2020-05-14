class Formula:

    def __init__(self, py_client, formula_json):
        self._py_client = py_client
        self._formula_json = formula_json

    def get_oid(self):
        """Get's the formula's Oid"""

        return self._formula_json['oid']

    def change_datasource(self, cube):
        """Change the data source of the formula.

        The formula must be re-added after a data source change for it to take effect

        Args:
             cube: The ElastiCube to set the formula to
        """
        self._formula_json['datasource'] = cube.get_metadata()

    def get_json(self):
        """Returns the formula json."""
        return self._formula_json
