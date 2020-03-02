import requests

from . import PySenseUtils


class Elasticube:

    def __init__(self, host, token, name):
        self._host = host
        self._token = token
        self._name = name

    def get_data_source_sql(self, path, query, file_type, *,
                            offset=None, count=None, include_metadata=None, is_masked_response=None):
        """
        Executes elasticube sql

        :param path: The location to save the file
        :param query: The query to execute
        :param file_type: File format to return
        :param offset: Defines how many items to skip before returning the results.
            For example, to return results from value #101 onward, enter a value of ‘100’.
        :param count: Limits the result set to a defined number of results. Enter 0 (zero) or leave blank not to limit.
        :param include_metadata: Whether to inlcude metadata.
        :param is_masked_response: Whether response should be masked.
        :return: The path of the created file
        """

        query = query.replace(' ', '%20')

        param_string = PySenseUtils.build_query_string({
            'query': query,
            'format': file_type,
            'offset': offset,
            'count': count,
            'includeMetadata': include_metadata,
            'isMaskedResponse': is_masked_response
        })

        resp = requests.get('{}/api/datasources/LocalHost/{}/sql?{}'.format(
            self._host, self._name, param_string), headers=self._token)
        PySenseUtils.parse_response(resp)
        output = resp.content.decode('utf-8-sig').splitlines()
        with open(path, "w") as file:
            for line in output:
                file.write(line + '\n')

        return path