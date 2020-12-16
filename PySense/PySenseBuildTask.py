class BuildTask:
    """Build Task

    Spawned when a build is triggered. Object is used to track and control an in progress build.

    Attributes:
        json (JSON): The JSON for this object
        py_client (PySense): The connection to the Sisense server which owns this asset
    """

    def __init__(self, py_client, build_task_json):
        """

        Args:
            py_client (PySense): The PySense object for the server this asset belongs to
            build_task_json (JSON): The json for this object
        """

        self.json = build_task_json
        self.py_client = py_client

    def get_oid(self):
        """Returns the oid of the build task"""

        return self.json['oid']

    def get_status(self):
        """Updates and returns the current status of the build object"""

        self.update()
        return self.json['status']

    def update(self):
        """Updates the build task with latest information from server"""

        self.json = self.py_client.connector.rest_call('get', 'api/v2/builds/{}'.format(self.get_oid()))

    def cancel_build(self):
        """Cancels build"""

        self.py_client.connector.rest_call('delete', 'api/v2/builds/{}'.format(self.get_oid()))

