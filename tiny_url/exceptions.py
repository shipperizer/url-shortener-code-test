class ResourceException(Exception):

    def __init__(self, message='Error', status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


class ResourceNotFound(ResourceException):

    def __init__(self, message='Resource not found', status_code=404, payload=None):
        super().__init__(message, status_code, payload)


class ResourceExists(ResourceException):

    def __init__(self, message='Resource exists', status_code=409, payload=None):
        super().__init__(message, status_code, payload)


class ResponseError(ResourceException):

    def __init__(self, message='Bad Response from the service', status_code=500, payload=None):
        super().__init__(message, status_code, payload)


class RequestError(ResourceException):

    def __init__(self, message='Bad Request', status_code=400, payload=None):
        super().__init__(message, status_code, payload)
