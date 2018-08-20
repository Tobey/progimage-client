class ProgImageClientException(Exception):
    pass


class ImageNotFound(ProgImageClientException):
    pass


class InvalidImage(ProgImageClientException):
    pass


class ApiException(ProgImageClientException):
    pass
