from __future__ import absolute_import, unicode_literals
import json
import requests

from .exceptions import EndpointNotFoundException, AttributeNotValidException, ConnectException, EmailNotFoundException, \
    NumberNotValidException, TokenNotFoundException, BadRequestException, UserNotAuthException
from .quotation_request import QuotationItem


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

    SMALL = 29
    MEDIUM = 49
    LARGE = 60
    LARGER = 999999

    PACKAGE_SIZES = (
        (SMALL, 'Pequeño (10x10x10cm)'),
        (MEDIUM, 'Mediano (30x30x30cm)'),
        (LARGE, 'Grande (50x50x50cm)'),
        (LARGER, 'Muy Grande (>60x60x60cm)'),
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
        """
        item = QuotationItem(request)
        quote = item.to_shipit_format()
        response = self.request(self.METHOD_POST, 'shippings/prices', quote)
        return response

    def best_quotation(self, request):
        """ Return quotation fastest and cheapest
        """
        item = QuotationItem(request)
        quote = item.to_shipit_format()
        response = self.request(self.METHOD_POST, 'shippings/price', quote)
        return response

    def economic_quotation(self, request):
        """ Return quotation cheapest
        """
        item = QuotationItem(request)
        quote = item.to_shipit_format()
        response = self.request(self.METHOD_POST, 'shippings/price', quote)
        return response

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
    def is_number(n):
        try:
            float(n)  # Type-casting the string to `float`.
            # If string is not a valid `float`,
            # it'll raise `ValueError` exception
        except ValueError:
            return False
        return True

    @staticmethod
    def package_size(width, height, length):
        if not Shipit.is_number(width) or not Shipit.is_number(height) or not Shipit.is_number(length):
            return None
        package_size = 0
        package_size = height if package_size < height else package_size
        package_size = width if package_size < width else package_size
        package_size = length if package_size < length else package_size
        test = Shipit.PACKAGE_SIZES
        for package_type in Shipit.PACKAGE_SIZES:
            if package_size < package_type[0]:
                return package_type[1]
        return None
