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
        """Test emitting an install hook."""
        self.harness.begin()
        self.harness.charm.on.install.emit()
        self.assertEqual(self.harness.charm.state.installed, True)


if __name__ == "__main__":
    unittest.main()
