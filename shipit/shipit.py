from __future__ import absolute_import
import json
import requests

from .exceptions import EndpointNotFoundException


class Shipit:
    ENV_DEVELOPMENT = 'development'
    ENV_PRODUCTION = 'production'
    endpoint = 'http://api.shipit.cl/v/'

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
        headers = {'Content-Type': 'application/json',
                   'X-Shipit-Email': self.email,
                   'X-Shipit-Access-Token': self.token,
                   'Accept': self.token,
                   }
        api_url = '{0}communeas'.format(self.endpoint)

        response = requests.get(api_url, headers=headers)
        if response.status_code == 404:
            raise EndpointNotFoundException('test')

        return json.loads(response.content.decode('utf-8'))

    # def get(self):
    #     if self.token == None:
    #         raise
