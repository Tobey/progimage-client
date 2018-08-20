from requests import Session
from requests import HTTPError

from . import exceptions


class ProgImageSession(Session):

    error_msg = 'An API error occurred. code [{}], reason [{}], details "{}"'

    def __init__(self, *, server_host, server_token, user_agent):
        super().__init__()
        self.api_url = server_host.rstrip('/') + '/images/'
        self.headers.update({
            'Authorization': f'Token {server_token}',
            'User-Agent': user_agent
        })

    def request(self, method, path, *args, transform=None, **kwargs):
        if path:
            path = path.rstrip('/') + '/'

        if transform:
            path += transform + '/'

        response = super().request(method, f'{self.api_url}{path}', *args, **kwargs)

        try:
            response.raise_for_status()
        except HTTPError:
            e = self.error_msg.format(
                response.status_code, response.reason, response.text
            )
            raise exceptions.ApiException(e)
        return response.json()
