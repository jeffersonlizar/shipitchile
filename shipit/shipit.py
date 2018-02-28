from __future__ import absolute_import, unicode_literals
import json
import requests
import datetime

from .exceptions import EndpointNotFoundException, AttributeNotValidException, ConnectException, EmailNotFoundException, \
    NumberNotValidException, TokenNotFoundException, BadRequestException, UserNotAuthException, DateFormatException


class Shipit:
    ENV_DEVELOPMENT = 'development'
    ENV_PRODUCTION = 'production'
    METHOD_POST = 'post'
    METHOD_GET = 'get'
    METHOD_PUT = 'put'
    base_api = 'http://api.shipit.cl/v/'

    email = None
    token = None

    environment = ENV_PRODUCTION

    SIZE_SMALL = 29
    SIZE_MEDIUM = 49
    SIZE_LARGE = 60
    SIZE_XLARGE = 999999

    PACKAGE_SIZES = (
        (SIZE_SMALL, 'Pequeño (10x10x10cm)'),
        (SIZE_MEDIUM, 'Mediano (30x30x30cm)'),
        (SIZE_LARGE, 'Grande (50x50x50cm)'),
        (SIZE_XLARGE, 'Muy Grande (>60x60x60cm)'),
    )

    PROVIDERS_TRAKING_URL = {
        'chilexpress': 'http://chilexpress.cl/Views/ChilexpressCL/Resultado-busqueda.aspx?DATA=:number',
        'starken': 'http://www.starken.cl/seguimiento?codigo=:number',
        'correoschile': 'http://www.correos.cl/SitePages/seguimiento/seguimiento.aspx?envio=:number'
    }

    def __init__(self, email, token, environment=ENV_PRODUCTION):
        self.email = email
        self.token = token
        if environment not in [self.ENV_PRODUCTION, self.ENV_DEVELOPMENT]:
            environment = self.ENV_PRODUCTION
        self.environment = environment

    def regions(self):
        """ Return regions available in shipit
        """
        regions = self.request(self.METHOD_GET, 'regions')
        return regions

    def communes(self):
        """ Return communes available in shipit
        """
        communes = self.request(self.METHOD_GET, 'communes')
        return communes

    def quotation(self, request):
        """ Return list of quotations
        Parameters
        ----------
        request : QuotationRequest
        """
        quote = request.to_shipit_format()
        response = self.request(self.METHOD_POST, 'shippings/prices', quote)
        return response

    def best_quotation(self, request):
        """ Return quotation fastest and cheapest
        Parameters
        ----------
        request : QuotationRequest
        """
        quote = request.to_shipit_format()
        response = self.request(self.METHOD_POST, 'shippings/price', quote)
        return response

    def economic_quotation(self, request):
        """ Return quotation cheapest
        Parameters
        ----------
        request : QuotationRequest
        """
        quote = request.to_shipit_format()
        response = self.request(self.METHOD_POST, 'shippings/price', quote)
        return response

    def request_shipping(self, request):
        """ Return shipping request
        Parameters
        ----------
        request : ShippingRequest
        """
        shipping = request.to_shipit_format(self.environment)
        data = {
            'package': shipping
        }
        response = self.request(self.METHOD_POST, 'packages', data)
        return response

    def request_massive_shipping(self, items):
        """ Return shipping request for multiple items
        Parameters
        ----------
        items : array ShippingRequest
        """
        data = {
            "packages": []
        }
        for item in items:
            data['packages'].append(item.to_shipit_format(self.environment))
        response = self.request(self.METHOD_POST, 'packages/mass_create', data)
        return response

    def all_shipping(self, date=None):
        """ Return history shipping for date
        Parameters
        ----------
        date : date
        """
        if not date:
            date = datetime.date.today()
        if not type(date).__name__ == 'date':
            raise DateFormatException(date)
        params = [
            'year={0}'.format(date.year),
            'month={0}'.format(date.month),
            'day={0}'.format(date.day),
        ]
        params_str = "&".join(str(x) for x in params)
        response = self.request(self.METHOD_GET, 'packages?' + params_str)
        return response

    def shipping(self, id=None):
        """ Return shipping detail
        Parameters
        ----------
        id : int
        """
        if not Shipit.is_int(id):
            raise NumberNotValidException(id)
        response = self.request(self.METHOD_GET, 'packages/' + str(id))
        return response

    @staticmethod
    def tracking_url(provider, tracking_number):
        if provider not in Shipit.PROVIDERS_TRAKING_URL:
            return None
        url = Shipit.PROVIDERS_TRAKING_URL[provider]
        return url.replace(':number', str(tracking_number))

    def request(self, method, endpoint, data=None):
        """ Returns the response of an endpoint
        Parameters
        ----------
        method : str
        endpoint : str
        data : Dict
        Returns
        -------
        response : JSON
            JSON object.
        """
        if not self.token:
            raise TokenNotFoundException
        if not self.email:
            raise EmailNotFoundException
        endpoint = '{0}{1}'.format(self.base_api, endpoint)
        headers = {'Content-Type': 'application/json',
                   'X-Shipit-Email': self.email,
                   'X-Shipit-Access-Token': self.token,
                   'Accept': 'application/vnd.shipit.v2',
                   }
        if method == self.METHOD_GET:
            res = requests.get(endpoint, headers=headers)
        elif method == self.METHOD_POST:
            res = requests.post(endpoint, json=data, headers=headers)
        else:
            res = requests.put(endpoint, json=data, headers=headers)
        if res.status_code == 400:
            raise BadRequestException()
        if res.status_code == 403:
            raise UserNotAuthException(self.email)
        if res.status_code == 404:
            raise EndpointNotFoundException(endpoint)
        response = json.loads(res.content.decode('utf-8'))
        return response

    @staticmethod
    def is_float(n):
        try:
            float(n)  # Type-casting the string to `float`.
            # If string is not a valid `float`,
            # it'll raise `ValueError` exception
        except ValueError:
            return False
        return True

    @staticmethod
    def is_int(n):
        try:
            int(n)  # Type-casting the string to `float`.
            # If string is not a valid `float`,
            # it'll raise `ValueError` exception
        except ValueError:
            return False
        return True

    @staticmethod
    def package_size(width, height, length):
        if not Shipit.is_float(width) or not Shipit.is_float(height) or not Shipit.is_float(length):
            raise NumberNotValidException()
        package_size = 0
        package_size = height if package_size < height else package_size
        package_size = width if package_size < width else package_size
        package_size = length if package_size < length else package_size
        test = Shipit.PACKAGE_SIZES
        for package_type in Shipit.PACKAGE_SIZES:
            if package_size < package_type[0]:
                return package_type[1]
        return None
