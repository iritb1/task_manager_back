class APIException(Exception):
    def __init__(self, code, message):
        self._code = code
        self._message = message

    @property
    def code(self):
        return self._code

    @property
    def message(self):
        return self._message

    # def __str__(self):
    #     return self.__class__.__name__ + ': ' + self.message


class ResourceNotFound(APIException):
    """Custom exception when resource is not found."""

    def __init__(self, resource_name, id):
        message = 'Resource {} {} not found'.format(resource_name, id)
        super().__init__(404, message)
