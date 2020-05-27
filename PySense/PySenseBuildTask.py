class BuildTask:

    def __init__(self, py_client, build_task_json):
        self._build_task_json = build_task_json
        self._py_client = py_client

    def get_oid(self):
        return self._build_task_json['oid']

    def get_status(self):
        self.update()
        return self._build_task_json['status']

    def update(self):
        """Updates the build task with latest information from server"""
        self._build_task_json = self._py_client.connector.rest_call('get', 'api/v2/builds/{}'.format(self.get_oid()))

    def cancel_build(self):
        """Cancels build"""
        self._py_client.connector.rest_call('delete', 'api/v2/builds/{}'.format(self.get_oid()))

