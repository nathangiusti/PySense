import unittest

import PySense.PySense as PySense


class PySensePluginTests(unittest.TestCase):
    def setUp(self):
        self.py_client = PySense.authenticate_by_file('C:\\PySense\\PySenseConfig.yaml')
        self.plugin = self.py_client.get_plugins(search='jumpToDashboard')[0]
        
    def test_enable_disable(self):
        assert self.plugin.get_is_enabled() is True
        self.plugin.set_plugin_enabled(False)
        self.plugin = self.py_client.get_plugins(search='jumpToDashboard')[0]
        assert self.plugin.get_is_enabled() is False
        self.plugin.set_plugin_enabled(True)
        assert self.plugin.get_is_enabled() is True
