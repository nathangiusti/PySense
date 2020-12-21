import unittest

from PySense import PySense


class PySensePluginTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.py_client = PySense.authenticate_by_file('resources//TestConfig.yaml')
        cls.plugin = cls.py_client.get_plugins(search='jumpToDashboard')[0]

    def test_enable_disable(self):
        enabled = self.plugin.get_is_enabled()
        self.plugin.set_plugin_enabled(not enabled)
        self.plugin = self.py_client.get_plugins(search='jumpToDashboard')[0]
        assert self.plugin.get_is_enabled() == (not enabled)
        self.plugin.set_plugin_enabled(enabled)
        assert self.plugin.get_is_enabled() == enabled

    def test_getters(self):
        assert self.plugin.get_name() is not None
        assert self.plugin.get_is_enabled() is not None
        assert self.plugin.get_version() is not None
        assert self.plugin.get_last_update() is not None

    def test_blox_actions(self):
        action = self.py_client.create_blox_action('Test Action', 'console.log()', 'Test Action')
        new_action = self.py_client.get_blox_action(action.get_type())
        self.py_client.delete_blox_actions(action)
        assert action.get_title() == new_action.get_title()
        assert action.get_body() == new_action.get_body()
        assert action.get_type() == new_action.get_type()

