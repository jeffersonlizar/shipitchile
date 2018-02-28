import unittest
from ..shipit import shipit


class TestShipitMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.shipit = shipit.Shipit('jlizarzabal@firesoft.com.ve', 'miRxLALSLWWv9fUC7KyW')

    def test_not_email_not_token(self):
        ship = shipit.Shipit('asdf', 'asdf')
        ship.email = None
        ship.token = None
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
