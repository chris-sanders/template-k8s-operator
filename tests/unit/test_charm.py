import unittest

import setuppath  # noqa:F401
from charm import ${class}
from ops.testing import Harness


class Test${class}(unittest.TestCase):
    def test_harness(self):
        """Verify harness."""
        harness = Harness(${class})
        harness.begin()
        self.assertFalse(harness.charm.state.installed)

    def test_install(self):
        """Test emitting an install hook."""
        harness.charm.on.install.emit()
        self.assertEqual(self.charm.state.installed, True)


if __name__ == "__main__":
    unittest.main()
