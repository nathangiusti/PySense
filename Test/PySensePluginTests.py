import unittest

from PySense import PySense


class PySensePluginTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.py_client = PySense.authenticate_by_file('//Users//nathan.giusti//Documents//PySense//VmConfig.yaml')
        cls.plugin = cls.py_client.get_plugins(search='jumpToDashboard')[0]
        cls.blox_action_name = 'PySenseTest'

    def test_enable_disable(self):
        assert self.plugin.get_is_enabled() is True
        self.plugin.set_plugin_enabled(False)
        self.plugin = self.py_client.get_plugins(search='jumpToDashboard')[0]
        assert self.plugin.get_is_enabled() is False
        self.plugin.set_plugin_enabled(True)
        assert self.plugin.get_is_enabled() is True

    def test_getters(self):
        assert self.plugin.get_name() is not None
        assert self.plugin.get_is_enabled() is not None
        assert self.plugin.get_version() is not None
        assert self.plugin.get_last_update() is not None

    def test_blox_actions(self):
        action = self.py_client.get_blox_action(self.blox_action_name)
        new_action = self.py_client.create_blox_action(action.get_type(), action.get_body(), action.get_title())
        self.py_client.delete_blox_action(self.blox_action_name)
        self.py_client.add_blox_action(new_action)
        new_action = self.py_client.get_blox_action(self.blox_action_name)
        assert action.get_title() == new_action.get_title()
        assert action.get_body() == new_action.get_body()
        assert action.get_type() == new_action.get_type()

