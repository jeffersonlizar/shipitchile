from .exceptions import AttributeNotValidException
from .shipit import Shipit


class ShippingRequest:
    SIZE_SMALL = 'Pequeño (10x10x10cm)'
    SIZE_MEDIUM = 'Mediano (30x30x30cm)'
    SIZE_LARGE = 'Grande (50x50x50cm)'
    SIZE_XLARGE = 'Muy Grande (>60x60x60cm)'

    PACKING_NONE = 'Sin empaque'
    PACKING_PAPERBOARD = 'Caja de Cartón'
    PACKING_PLASTIC = 'Film Plástico'
    PACKING_BURBLE = 'Caja + Burbuja'
    PACKING_KRAFT = 'Papel Kraft'

    DELIVERY_NORMAL = 'Normal'
    DELIVERY_SATURDAY = 'Sábado'
    DELIVERY_SUNDAY = 'Domingo'

    DESTINATION_HOME = 'Domicilio'
    DESTINATION_CHILEXPRESS = 'Chilexpress'
    DESTINATION_STARKEN = 'Starken-Turbus'

    COURIER_NONE = ''
    COURIER_CHILEXPRESS = 'Chilexpress'
    COURIER_STARKEN = 'Starken'

    valid_properties = [
        'reference',
        'full_name',
        'email',
        'items_count',
        'cellphone',
        'is_payable',
        'packing',
        'shipping_type',
        'destiny',
        'courier_for_client',
        'approx_size',
        'address_commune_id',
        'address_street',
        'address_number',
        'address_complement',
    ]

    def __init__(self, data):
        self.data = {
            'reference': None,
            'full_name': None,
            'email': None,
            'items_count': None,
            'cellphone': None,
            'is_payable': False,
            'packing': None,
            'shipping_type': None,
            'destiny': 'Domicilio',
            'courier_for_client': None,
            'approx_size': None,
            'address_commune_id': None,
            'address_street': None,
            'address_number': None,
            'address_complement': None,
            'address_coords_latitude': None,
            'address_coords_longitude': None,
        }
        for key in data:
            if key not in self.valid_properties:
                raise AttributeNotValidException(key)
            self.data[key] = data[key]

    def to_shipit_format(self, environment=Shipit.ENV_PRODUCTION):
        if environment == Shipit.ENV_DEVELOPMENT:
            self.data['reference'] = 'TEST-{0}'.format(self.data['reference'])

        self.data['address_attributes'] = {
            'commune_id': self.data['address_commune_id'],
            'street': self.data['address_street'],
            'number': self.data['address_number'],
            'complement': self.data['address_complement'],
            # 'coords': {
            #     'latitude': self.data['address_coords_latitude'],
            #     'longitude': self.data['address_coords_longitude'],
            # }
        }

        del self.data['address_commune_id']
        del self.data['address_street']
        del self.data['address_number']
        del self.data['address_complement']
        del self.data['address_coords_latitude']
        del self.data['address_coords_longitude']

        return self.data
