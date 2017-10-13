
class FormatoIncorrecto(Exception):
    def __init__(self, message=''):
        super(FormatoIncorrecto, self).__init__(message)