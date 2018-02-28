class EndpointNotFoundException(Exception):
    """Raise for my specific kind of exception"""

    def __init__(self, endpoint):
        self.endpoint = endpoint
        super(EndpointNotFoundException, self).__init__()

    def __str__(self):
        return 'Endpoint not found {0}'.format(self.endpoint)


class UserNotAuthException(Exception):
    """Raise for my specific kind of exception"""

    def __init__(self, user):
        self.user = user
        super(UserNotAuthException, self).__init__()

    def __str__(self):
        return 'User not authenticated {0}'.format(self.user)


class BadRequestException(Exception):
    """Raise for my specific kind of exception"""

    def __init__(self):
        super(BadRequestException, self).__init__()

    def __str__(self):
        return 'Bad Request'


class DateFormatException(Exception):
    """Raise for my specific kind of exception"""

    def __init__(self, date):
        self.date = date
        super(DateFormatException, self).__init__()

    def __str__(self):
        return 'Incorrect data, {0} must be a date object'.format(self.date)


class AttributeNotValidException(Exception):
    """Raise for my specific kind of exception"""

    def __init__(self, attribute):
        self.attribute = attribute
        super(AttributeNotValidException, self).__init__()

    def __str__(self):
        return 'Attribute not valid {0}'.format(self.attribute)


class ConnectException(Exception):
    """Raise for my specific kind of exception"""

    def __init__(self, endpoint):
        self.endpoint = endpoint
        super(ConnectException, self).__init__()

    def __str__(self):
        return 'Could not resolve host {0}'.format(self.endpoint)


class EmailNotFoundException(Exception):
    """Raise for my specific kind of exception"""

    def __str__(self):
        return 'Email not found'


class NumberNotValidException(Exception):
    """Raise for my specific kind of exception"""

    def __init__(self, number = None):
        self.number = number
        super(NumberNotValidException, self).__init__()

    def __str__(self):
        return 'Number not valid {0}'.format(self.number)


class TokenNotFoundException(Exception):
    """Raise for my specific kind of exception"""

    def __str__(self):
        return 'Token not found'
