import os
from uuid import UUID

from . import exceptions
from . import config
from . import session


class ProgImageClient:
    valid_image_extensions = (
        'png',
        'jpeg',
        'svg',
    )

    def __init__(self,
                 server_host=config.DEFAULT_SERVER_HOST,
                 server_token=config.DEFAULT_SERVER_TOKEN,
                 user_agent='ProgImage-Client'):

        super().__init__()

        self.api_url = f'{server_host}/images'
        self.session = session.ProgImageSession(server_host=server_host,
                                                server_token=server_token,
                                                user_agent=user_agent)

    def get_one(self, image_id: str):
        """
        Retrieve image from server

        :param image_id: image uuid
        :return:
        """
        self._validate_uuids([image_id])

        response = self.session.get(image_id)
        return response

    def get_many(self, image_ids: list, transform=None):
        """
        Retrieve image from server

        :param image_id: image uuid
        :param transform: transform type
        :return:
        """

        self._validate_uuids(image_ids)

        image_ids = ','.join(image_ids)

        response = self.session.get('', params=dict(id__in=image_ids), transform=transform)
        return response['results']

    def upload_one(self, image_path: str):
        """
        Saves image to DB and return unique identifier

        :param image_path: path to image file
        :return:
        """


        self._valid_path([image_path])
        self._valid_ext([image_path])

        files = {'media': open(image_path, 'rb')}
        response = self.session.post('', files=files)

        return response

    def upload_many(self, image_paths: list):
        """
        Saves image to DB and return unique identifier

        :param image_path: path to image file
        :return:
        """

        self._valid_path(image_paths)
        self._valid_ext(image_paths)
        files = [('image', open(image_path, 'rb')) for image_path in image_paths]

        response = self.session.post('', files=files)

        return response

    @staticmethod
    def _valid_path(file_paths: list):
        for file_path in file_paths:
            if not os.path.exists(file_path):
                raise exceptions.ImageNotFound(f'File not found "{file_path}"')

    def _valid_ext(self, file_paths: list):
        for file_path in file_paths:
            file_ext = file_path.rsplit('.', 1)[-1]
            if file_ext not in self.valid_image_extensions:
                raise exceptions.InvalidImage(f'Give image file ending in {self.valid_image_extensions}')
    @staticmethod
    def _validate_uuids(uuids: list):
        for u in uuids:
            try:
                #  validate ID to save api calls to server
                UUID(u, version=4)
            except Exception:
                raise exceptions.ProgImageClientException(
                    'image id must be a valid version 4 uuid'
                )


prog_image_client = ProgImageClient()
