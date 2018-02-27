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

---- Under Construction ----


Do not hesitate to send me your feedbacks or pull-request to improve this library.

Thanks
=============

Thanks to kattatzu for create the initial version for php https://github.com/kattatzu/ShipIt

Licencia
=============

MIT License

Copyright (c) 2018 Jefferson Lizarzabal

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.