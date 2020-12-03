from PySense import PySenseBloxAction, PySensePlugin


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

    def get_blox_action(self, type):
        """Returns the blox action with the given type

        Args:
            type: The name of your blox action
        """
        json_payload = {
            "type": type
        }
        resp = self.connector.rest_call('post', 'api/v1/getActionByType/Blox', json_payload=json_payload)
        return PySenseBloxAction.BloxAction(self, resp)

    def create_blox_action(self, type, body, title):
        """Create a new PySense BloxAction object that can be imported

        Running this method will only create the action locally.
        The action must still be added to the server via add_blox_action

        Args:
            type: What you would like to call your blox action
            body: The raw javascript of the blox action
            title: The default text you would want to appear on a button using this action
        """
        action_json = {
            "type": type,
            "body": body,
            "snippet": {
                "type": type,
                "title": title
            }
        }
        return PySenseBloxAction.BloxAction(self, action_json)

    def delete_blox_action(self, action_type):
        """Deletes the blox action with the given action_type

        Args:
            action_type: The type (name as it appears in blox) action to delete
        """
        json_payload = {
            "type": action_type
        }
        self.connector.rest_call('post', 'api/v1/deleteCustomAction/Blox', json_payload=json_payload)

    def add_blox_action(self, blox_action):
        """Add a new blox custom action

        Args:
           blox_action: The PySense BloxAction object to add. Must be an object, not raw JSON.
        """
        self.connector.rest_call('post', '/api/v1/saveCustomAction/BloX', json_payload=blox_action.get_json())