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

    data = {}

    def __init__(self, data):
        for key in data:
            if key not in self.valid_properties:
                raise AttributeNotValidException(key)
            self.data[key] = data[key]

    def to_shipit_format(self):
        self.data['address_attributes'] = {
            "commune_id": self.data['commune_id']
        }
        del self.data['commune_id']
        package = {
            "package": self.data
        }
        return package
