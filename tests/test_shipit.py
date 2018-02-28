from __future__ import absolute_import, unicode_literals
import unittest
from shipit.shipit import Shipit
import sys

# sys.path.append("..")
# from ..shipit.shipit import Shipit


class TestShipitMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.shipit = Shipit('jlizarzabal@firesoft.com.ve', 'miRxLALSLWWv9fUC7KyW')

    def test_not_email_not_token(self):
        shipit = Shipit('email', 'token')
        shipit.email = None
        shipit.token = None
        regions = self.shipit.regions()
        self.assertIsNotNone(regions)
        self.assertNotIn('error', regions)

    def test_regions(self):
        regions = self.shipit.regions()
        self.assertIsNotNone(regions)
        self.assertNotIn('error', regions)

    def test_communes(self):
        communes = self.shipit.communes()
        self.assertIsNotNone(communes)
        self.assertNotIn('error', communes)
