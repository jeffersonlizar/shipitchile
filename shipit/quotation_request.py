from .exceptions import AttributeNotValidException


class QuotationRequest:
    valid_properties = [
        'length',
        'width',
        'height',
        'weight',
        'destiny',
        'courrier_for_client',
        'is_payable',
        'commune_id',
    ]

    def __init__(self, data):
        self.data = {
            'commune_id': None,
            'courrier_for_client': None,
            'destiny': "Domicilio",
            'height': 0,
            # "is_payable": False,
            'length': 0,
            'weight': 0,
            'width': 0
        }
        for key in data:
            if key not in self.valid_properties:
                raise AttributeNotValidException(key)
            self.data[key] = data[key]

    def to_shipit_format(self):
        self.data['address_attributes'] = {
            'commune_id': self.data['commune_id']
        }
        del self.data['commune_id']
        package = {
            'package': self.data
        }
        return package
