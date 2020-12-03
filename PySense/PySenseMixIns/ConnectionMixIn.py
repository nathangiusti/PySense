from PySense import PySenseConnection, PySenseUtils


class ConnectionMixIn:

    def get_connections(self, *, provider=None, sort=None, skip=None, limit=None):
        """Returns all the connections

        Args:
            provider: Type or list of types to filter for
            sort: Field by which the results should be sorted. Ascending by default, descending if prefixed by -
            skip: Number of results to skip from the start of the data set.
                Skip is to be used with the limit parameter for paging
            limit: How many results should be returned. limit is to be used with the skip parameter for paging
        """
        query_params = {
            'sort': sort,
            'skip': skip,
            'limit': limit
        }
        provider = PySenseUtils.make_iterable(provider)
        resp_json = self.connector.rest_call('get', 'api/v1/connection', query_params=query_params)
        ret_arr = []
        for connection in resp_json:
            connection = PySenseConnection.Connection(self, connection)
            if len(provider) > 0:
                if connection.get_provider() in provider:
                    ret_arr.append(connection)
            else:
                ret_arr.append(connection)
        return ret_arr

    def get_connection_by_id(self, connection_id):
        """Returns the connection with the given id"""
        resp_json = self.connector.rest_call('get', 'api/v1/connection/{}'.format(connection_id))
        return PySenseConnection.Connection(self, resp_json)

    def add_connection(self, connection_json):
        """Adds a new connection with given connection json. Returns the new connection"""
        resp_json = self.connector.rest_call('post', 'api/v1/connection', json_payload=connection_json)
        return PySenseConnection.Connection(self, resp_json)

    def delete_connections(self, connections):
        """Deletes the given PySense connections"""
        for connection in PySenseUtils.make_iterable(connections):
            self.connector.rest_call('delete', 'api/v1/connection/{}'.format(connection.get_oid()))