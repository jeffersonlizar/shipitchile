Shipit
########################################

Library that allows integration with the Shipit API (https://developers.shipit.cl/docs) for
Send dispatch requests, check your statements and other actions.

Access Credentials
=============

To use the Shipit API you must have an account and access the "API" menu to
Copy your email and access token.

https://clientes.shipit.cl/settings/api


Use
=============


.. code-block:: python

    shipit = new Shipit('EMAIL', 'TOKEN', 'development')
    // o
    shipit = new Shipit()
    shipit.email('EMAIL')
    shipit.token('TOKEN')
    shipit.environment(Shipit.ENV_PRODUCTION)

    print(Shipit.communes())

Available Actions
=============

Obtain the Regions and Communes
-----

You can list the regions and communes that Shipit has registered to synchronize
your system

.. code-block:: python

    shipit.regions()
    shipit.communes()

Example
-----

.. code-block:: python

    regions = shipit.regions()
    print(regions[0]['name'])
    // "Arica y Parinacota"


Get a Quote
-----

You can send the information of your office and get a quote with the options
of cariers available Shipit.

For this it is necessary that you create an instance ** QuotationRequest ** to be sent to the method ** quotation **.

Example
-----

.. code-block:: python

    data = QuotationRequest({
        "length": 1,
        "width": 1,
        "height": 1,
        "weight": 1,
        "destiny": "Domicilio",
        "is_payable": "false",
        "commune_id": 295
    })
    items = shipit.quotation(data)
    for item in items['shipments']:
        print(item['courier'])

Get the Most Economic Quote
-----

You can send the information of your office and get the cheapest quote.

.. code-block:: python

    data = QuotationRequest({
        "length": 1,
        "width": 1,
        "height": 1,
        "weight": 1,
        "destiny": "Domicilio",
        "is_payable": "false",
        "commune_id": 295
    })
    item = shipit.economic_quotation(data)
    print(item['shipment']['total'])

Get the Most Convenient Quote
-----

You can get the most convenient quote in both response time (SLA) and price.

.. code-block:: python

    data = QuotationRequest({
        "length": 1,
        "width": 1,
        "height": 1,
        "weight": 1,
        "destiny": "Domicilio",
        "is_payable": "false",
        "commune_id": 295
    })
    item = shipit.best_quotation(data)
    print(item['shipment']['total'])

Send a Shipping request
-----

To send a shipping request you must create an ** ShippingRequest ** instance to be sent to the ** request_shipping ** method:

.. code-block:: python

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
    shipping = shipit.request_shipping(data)
    print(shipping['id'])

Send a Shipping request for multiple items
-----

To send a shipping request you must create an ** ShippingRequest ** instance to be sent to the ** request_shipping ** method:

.. code-block:: python

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
    shipping = shipit.request_massive_shipping(shipping_list)

Show shipping detail
-----

You can consult the data of a historical shipping by sending the id delivered by Shipit
using the ** shipping ** method:

.. code-block:: python

    shipping = shipit.shipping(280584)
    print(shipping['id'])
    print(shipping['reference])

Show shipping requests history
-----

You can check the history of shipping made per day using the ** all_shipping ** method:
By default it will be the current date

.. code-block:: python

    date = datetime.date(2018, 1, 26)
    shipping = shipit.all_shipping(date)
    for shipping_data in shipping:
        print(shipping_data['id'])


Utilities
=============

Obtain tracking URL
-----

You can generate the tracking url easily:

.. code-block:: python
    test = Shipit.tracking_url('chilexpress', 99680722912)

Approximate shipping size
-----

You can get the approximate size in the Shipit format of a package.

.. code-block:: python
    size = Shipit.package_size(width = 14, height = 23, length = 45)

---- Under Construction ----


Do not hesitate to send me your feedbacks or pull-request to improve this library.

Thanks
=============

Thanks to kattatzu for create the original version for PHP https://github.com/kattatzu/ShipIt

Licence
=============

MIT License

Copyright (c) 2018 Jefferson Lizarzabal

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.