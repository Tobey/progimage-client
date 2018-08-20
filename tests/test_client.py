import os
import unittest
from unittest import TestCase
from unittest import mock
from uuid import uuid4


from . import test_data
from proxy_store_request import prog_image_client
from proxy_store_request import tranforms


root_dir = os.path.dirname(os.path.abspath(__file__))


class FakeResponse:

    def __init__(self, data, status_code):
        self.data = data
        self.status_code = status_code

    def json(self):
        return self.data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception


class TestClient(TestCase):

    @property
    def uuid(self):
        return str(uuid4())

    @mock.patch('requests.Session.request')
    def test_get_one(self, request_mock):
        request_mock.return_value = FakeResponse(test_data.get_one_response, 200)

        uuid = self.uuid
        response = prog_image_client.get_one(uuid)

        request_mock.assert_called_with(
            'GET', f'http://localhost:8000/images/{uuid}/', allow_redirects=True
        )
        self.assertDictEqual(test_data.get_one_response, response)

    @mock.patch('requests.Session.request')
    def test_get_many(self, request_mock):
        request_mock.return_value = FakeResponse(test_data.get_many_response, 200)

        uuid = self.uuid
        response = prog_image_client.get_many([uuid])
        request_mock.assert_called_with(
            'GET', 'http://localhost:8000/images/', allow_redirects=True,
            params={'id__in': uuid}
        )
        self.assertListEqual(test_data.get_many_response['results'], response)

    @mock.patch('requests.Session.request')
    def test_upload_one(self, request_mock):
        request_mock.return_value = FakeResponse(test_data.get_one_response, 201)
        image_path = os.path.join(root_dir, 'test_image.png')
        prog_image_client.upload_one(image_path)

        self.assertListEqual(list(request_mock.call_args[0]), ['POST', 'http://localhost:8000/images/'])
        self.assertEqual(request_mock.call_args[1]['files']['media'].name, image_path)

    @mock.patch('requests.Session.request')
    def test_upload_many(self, request_mock):
        request_mock.return_value = FakeResponse(test_data.get_one_response, 201)

        image_paths = os.path.join(root_dir, 'test_image.png')
        image_paths = [image_paths] * 2
        prog_image_client.upload_many(image_paths)

        uploaded_files = [file[1].name for file in request_mock.call_args[1]['files']]
        self.assertListEqual(list(request_mock.call_args[0]), ['POST', 'http://localhost:8000/images/'])
        self.assertListEqual(uploaded_files, image_paths)

    @mock.patch('requests.Session.request')
    def test_get_thumbnails(self, request_mock):
        request_mock.return_value = FakeResponse(test_data.get_many_response, 200)

        uuid = self.uuid
        response = prog_image_client.get_many([uuid], transform=tranforms.THUMBNAIL)

        request_mock.assert_called_with(
            'GET', 'http://localhost:8000/images/thumbnail/', allow_redirects=True,
            params={'id__in': uuid}
        )
        self.assertListEqual(test_data.get_many_response['results'], response)


if __name__ == '__main__':
    unittest.main()
