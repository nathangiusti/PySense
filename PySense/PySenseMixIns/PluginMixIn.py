from PySense import PySenseBloxAction, PySensePlugin, PySenseUtils


class PluginMixIn:

    def get_plugins(self, *, order_by=None, desc=None, search=None, skip=None, limit=None):
        """Get all plugins installed.

        Args:
            order_by (str): (Optional) Filter by provided field
            desc (bool): (Optional) Order by descending/ascending (boolean)
            search (str): (Optional) Filter according to provided string
            skip (int): (Optional) Number of results to skip from the start of the data set.
                Skip is to be used with the limit parameter for paging.
            limit (int): (Optional) How many results should be returned.
                Limit is to be used with the skip parameter for paging

        Returns:
            list[PlugIn]: Found plugins
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

    def get_blox_action(self, action_type):
        """Returns the blox action with the given type

        Args:
            action_type (str): The name of your blox action

        Returns:
            BloxAction: The blox action with the given type
        """

        json_payload = {
            "type": action_type
        }
        resp = self.connector.rest_call('post', 'api/v1/getActionByType/Blox', json_payload=json_payload)
        return PySenseBloxAction.BloxAction(self, resp)

    def create_blox_action(self, action_type, body, title):
        """Create a new PySense BloxAction object and adds it to server

        Args:
            action_type (str): What you would like to call your blox action
            body (str): The raw javascript of the blox action
            title (str): The default text you would want to appear on a button using this action

        Returns:
            BloxAction: The new BloxAction that has been added
        """

        action_json = {
            "type": action_type,
            "body": body,
            "snippet": {
                "type": action_type,
                "title": title
            }
        }
        blox_action = PySenseBloxAction.BloxAction(self, action_json)
        self.connector.rest_call('post', '/api/v1/saveCustomAction/BloX', json_payload=blox_action.json)
        return blox_action

    def delete_blox_actions(self, actions):
        """Deletes the blox actions

        Args:
            actions (list[BloxAction]): Actions to delete
        """

        for action in PySenseUtils.make_iterable(actions):
            json_payload = {
                "type": action.get_type()
            }
            self.connector.rest_call('post', 'api/v1/deleteCustomAction/Blox', json_payload=json_payload)

    def add_blox_action(self, blox_action):
        """Add a new blox custom action

        Args:
           blox_action (BloxAction): The PySense BloxAction object to add. Must be an object, not raw JSON.
        """

        self.connector.rest_call('post', '/api/v1/saveCustomAction/BloX', json_payload=blox_action.json)