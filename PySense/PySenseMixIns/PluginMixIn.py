from PySense import PySensePlugin


class PluginMixIn:

    def get_plugins(self, *, order_by=None, desc=None, search=None, skip=None, limit=None):
        """Get all plugins installed.

        Args:
            order_by: (optional) Filter by provided field
            desc: (optional) Order by descending/ascending (boolean)
            search: (optional) Filter according to provided string
            skip: (optional) Number of results to skip from the start of the data set.
                Skip is to be used with the limit parameter for paging.
            limit: (optional) How many results should be returned. limit is to be used with the skip parameter for paging

        Returns:
            An array of plugins
        """
        query_params = {
            'orderby': order_by,
            'desc': desc,
            'search': search,
            'skip': skip,
            'limit': limit
        }
        resp_json = self.connector.rest_call('get', 'api/v1/plugins', query_params=query_params)
        ret_arr = []
        for plugin in resp_json['plugins']:
            ret_arr.append((PySensePlugin.Plugin(self, plugin)))
        return ret_arr