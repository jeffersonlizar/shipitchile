from __future__ import absolute_import
import json
import requests

from .exceptions import EndpointNotFoundException, AttributeNotValidException, ConnectException, EmailNotFoundException, \
    NumberNotValidException, TokenNotFoundException, BadRequestException, UserNotAuthException


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

    def __init__(self, email, token, environment=ENV_PRODUCTION):
        self.email = email
        self.token = token
        if environment not in [self.ENV_PRODUCTION, self.ENV_DEVELOPMENT]:
            environment = self.ENV_PRODUCTION
        self.environment = environment

    def regions(self):
        regions = self.request(self.METHOD_GET, 'communes')
        return regions

    def regions(self):
        regions = self.request(self.METHOD_GET, 'communes')
        return regions

    def request(self, method, endpoint, data=None):
        if not self.token:
            raise TokenNotFoundException
        if not self.email:
            raise EmailNotFoundException
        endpoint = '{0}{1}'.format(self.base_api, endpoint)
        try:
            headers = {'Content-Type': 'application/json',
                       'X-Shipit-Email': self.email,
                       'X-Shipit-Access-Token': self.token,
                       'Accept': 'application/vnd.shipit.v2',
                       }
            if method == self.METHOD_GET:
                res = requests.get(endpoint, headers=headers)
            elif method == self.METHOD_POST:
                res = requests.post(endpoint, data=data, headers=headers)
            else:
                res = requests.put(endpoint, data=data, headers=headers)
            if res.status_code == 400:
                raise BadRequestException()
            if res.status_code == 404:
                raise EndpointNotFoundException(endpoint)
            if res.status_code == 403:
                raise UserNotAuthException(self.email)
            response = json.loads(res.content.decode('utf-8'))
        except Exception:
            raise ConnectException(endpoint)
        return response
