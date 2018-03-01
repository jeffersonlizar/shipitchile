#!/usr/bin/python
from __future__ import absolute_import

import unittest
import datetime

from shipit import Shipit, QuotationRequest, ShippingRequest

# for test local dev
# from ..shipit import Shipit, QuotationRequest, ShippingRequest


class TestShipitMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.shipit = Shipit('jlizarzabal@firesoft.com.ve', 'miRxLALSLWWv9fUC7KyW', Shipit.ENV_DEVELOPMENT)

    def test_not_email_not_token(self):
        shipit = Shipit('email', 'token')
        shipit.email = None
        shipit.token = None
        regions = self.shipit.regions()
        self.assertIsNotNone(regions)
        self.assertIsInstance(regions, list)
        self.assertNotIn('error', regions)

    def test_regions(self):
        regions = self.shipit.regions()
        self.assertIsNotNone(regions)
        self.assertIsInstance(regions, list)
        self.assertNotIn('error', regions)

    def test_communes(self):
        communes = self.shipit.communes()
        self.assertIsNotNone(communes)
        self.assertIsInstance(communes, list)
        self.assertNotIn('error', communes)

    def test_quotation(self):
        data = QuotationRequest({
            "length": 1,
            "width": 1,
            "height": 1,
            "weight": 1,
            "destiny": "Domicilio",
            "is_payable": "false",
            "commune_id": 295
        })
        items = self.shipit.quotation(data)
        self.assertIsNotNone(items)
        self.assertIsInstance(items, dict)
        self.assertIn('shipments', items)
        self.assertNotIn('error', items)

    def test_quotation_error_commune(self):
        data = QuotationRequest({
            "length": 1,
            "width": 1,
            "height": 1,
            "weight": 1,
            "destiny": "Domicilio",
            "is_payable": "false",
            "commune_id": 0
        })
        items = self.shipit.quotation(data)
        self.assertIsNotNone(items)
        self.assertIsInstance(items, dict)
        self.assertIn('error', items)

    def test_best_quotation(self):
        data = QuotationRequest({
            "length": 1,
            "width": 1,
            "height": 1,
            "weight": 1,
            "destiny": "Domicilio",
            "is_payable": "false",
            "commune_id": 295
        })
        items = self.shipit.best_quotation(data)
        self.assertIsNotNone(items)
        self.assertIsInstance(items, dict)
        self.assertIn('shipment', items)
        self.assertIn('total', items['shipment'])
        self.assertNotIn('error', items)

    def test_economic_quotation(self):
        data = QuotationRequest({
            "length": 1,
            "width": 1,
            "height": 1,
            "weight": 1,
            "destiny": "Domicilio",
            "is_payable": "false",
            "commune_id": 295
        })
        items = self.shipit.economic_quotation(data)
        self.assertIsNotNone(items)
        self.assertIsInstance(items, dict)
        self.assertIn('shipment', items)
        self.assertIn('total', items['shipment'])
        self.assertNotIn('error', items)

    def test_request_shipping(self):
        data = ShippingRequest({
            "reference": "S000001",
            "full_name": "Jefferson Lizarzabal",
            "email": "cliente@gmail.com",
            "items_count": 1,
            "cellphone": "912341234",
            "is_payable": False,
            "packing": ShippingRequest.PACKING_NONE,
            "shipping_type": ShippingRequest.DELIVERY_NORMAL,
            "destiny": ShippingRequest.DESTINATION_HOME,
            "courier_for_client": ShippingRequest.COURIER_CHILEXPRESS,
            "approx_size": ShippingRequest.SIZE_SMALL,
            "address_commune_id": 317,
            "address_street": "San Carlos",
            "address_number": 123,
            "address_complement": None
        })
        shipping = self.shipit.request_shipping(data)
        self.assertIsNotNone(shipping)
        self.assertIsInstance(shipping, dict)
        self.assertIn('id', shipping)
        self.assertNotIn('error', shipping)
        self.shipping_id = shipping['id']

    def test_request_massive_shipping(self):
        shipping_list = []
        shipping_1 = ShippingRequest({
            "reference": "S000002",
            "full_name": "Jefferson Lizarzabal",
            "email": "cliente@gmail.com",
            "items_count": 1,
            "cellphone": "912341234",
            "is_payable": False,
            "packing": ShippingRequest.PACKING_NONE,
            "shipping_type": ShippingRequest.DELIVERY_NORMAL,
            "destiny": ShippingRequest.DESTINATION_HOME,
            "courier_for_client": ShippingRequest.COURIER_CHILEXPRESS,
            "approx_size": ShippingRequest.SIZE_SMALL,
            "address_commune_id": 317,
            "address_street": "San Carlos",
            "address_number": 123,
            "address_complement": None
        })
        shipping_list.append(shipping_1)
        shipping_2 = ShippingRequest({
            "reference": "S000003",
            "full_name": "Jefferson Lizarzabal",
            "email": "cliente@gmail.com",
            "items_count": 1,
            "cellphone": "912341234",
            "is_payable": False,
            "packing": ShippingRequest.PACKING_NONE,
            "shipping_type": ShippingRequest.DELIVERY_NORMAL,
            "destiny": ShippingRequest.DESTINATION_HOME,
            "courier_for_client": ShippingRequest.COURIER_CHILEXPRESS,
            "approx_size": ShippingRequest.SIZE_SMALL,
            "address_commune_id": 317,
            "address_street": "San Carlos",
            "address_number": 123,
            "address_complement": None
        })
        shipping_list.append(shipping_2)
        shipping = self.shipit.request_massive_shipping(shipping_list)
        self.assertIsInstance(shipping, dict)
        self.assertIsNotNone(shipping)
        self.assertIn('message', shipping)
        self.assertNotIn('error', shipping)

    def test_shipping_detail(self):
        self.test_request_shipping()
        shipping = self.shipit.shipping(self.shipping_id)
        self.assertIsNotNone(shipping)
        self.assertIsInstance(shipping, dict)
        self.assertIn('id', shipping)
        self.assertIn('reference', shipping)
        self.assertNotIn('error', shipping)

    def test_shipping_history(self):
        history = self.shipit.all_shipping()
        self.assertIsInstance(history, list)
        self.assertIsNotNone(history)
        self.assertNotIn('error', history)

    def test_shipping_history_specific_date(self):
        date = datetime.date(2018, 1, 25)
        history = self.shipit.all_shipping(date)
        self.assertIsInstance(history, list)
        self.assertIsNotNone(history)
        self.assertNotIn('error', history)

    def test_tracking_url(self):
        tracking_url = Shipit.tracking_url('chilexpress', 99680722912)
        self.assertIsInstance(tracking_url, str)
        self.assertEqual(tracking_url,
                         'http://chilexpress.cl/Views/ChilexpressCL/Resultado-busqueda.aspx?DATA=99680722912')
        self.assertIsNotNone(tracking_url)

    def test_package_size(self):
        size = Shipit.package_size(width=14, height=23, length=45)
        self.assertIsInstance(size, str)
        self.assertIsNotNone(size)
