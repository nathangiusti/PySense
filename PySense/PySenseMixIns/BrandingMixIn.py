from PySense import PySenseBranding


class BrandingMixIn:
    def get_branding(self):
        """Returns the current branding"""
        
        return PySenseBranding.Branding(self.connector, self.connector.rest_call('get', 'api/branding'))

    def set_branding(self, branding):
        """Update the branding
        Args:
            branding (Branding): The PySense Branding object
        """

        self.connector.rest_call('post', 'api/branding', json_payload=branding.json)
