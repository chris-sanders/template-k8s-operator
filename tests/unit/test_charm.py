import unittest

import setuppath  # noqa:F401
from charm import ${class}
from ops.testing import Harness


class Test${class}(unittest.TestCase):

    def setUp(self):
        """Setup tests."""
        self.harness = Harness(${class})

    def test_harness(self):
        """Verify harness."""
        self.harness.begin()
        self.assertFalse(self.harness.charm.state.installed)

    def test_install(self):
        """Test response to an install event."""
        self.harness.begin()
        self.harness.charm.on.install.emit()
        self.assertTrue(self.harness.charm.state.installed)

    # This pattern can't work before juju 2.8
    # def test_config_changed_not_installed(self):
    #     """Test response to config changed event without install state."""
    #     self.harness.begin()
    #     self.harness.charm.on.config_changed.emit()
    #     self.assertFalse(self.harness.charm.state.configured)

    def test_config_changed(self):
        """Test response to config changed event."""
        self.harness.set_leader(True)
        self.harness.begin()
        self.harness.charm.state.installed = True
        self.harness.charm.on.config_changed.emit()
        self.assertTrue(self.harness.charm.state.configured)

    def test_start_not_installed(self):
        """Test response to start event without install state."""
        self.harness.begin()
        self.harness.charm.on.start.emit()
        self.assertFalse(self.harness.charm.state.started)

    def test_start_not_configured(self):
        """Test response to start event without configured state."""
        self.harness.begin()
        self.harness.charm.state.installed = True
        self.harness.charm.on.start.emit()
        self.assertFalse(self.harness.charm.state.started)

    def test_start(self):
        """Test response to start event."""
        self.harness.begin()
        self.harness.charm.state.installed = True
        self.harness.charm.state.configured = True
        self.harness.charm.on.start.emit()
        self.assertTrue(self.harness.charm.state.started)


if __name__ == "__main__":
    unittest.main()
