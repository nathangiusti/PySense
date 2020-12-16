class SettingsMixIn:

    def get_ui_settings(self):
        """Returns the current ui settings as raw JSON"""

        return self.connector.rest_call('get', 'api/v1/settings/ui')

    def set_ui_settings(self, ui_settings):
        """Update the ui settings
        Args:
            ui_settings (JSON): A json blob of ui settings
        """

        self.connector.rest_call('post', 'api/v1/settings/ui/common', json_payload=ui_settings)
