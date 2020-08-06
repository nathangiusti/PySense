import unittest

import PySense.PySense as PySense


class PySensePluginTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.py_client = PySense.authenticate_by_file('C:\\PySense\\VmConfig.yaml')
        cls.plugin = cls.py_client.get_plugins(search='jumpToDashboard')[0]

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
