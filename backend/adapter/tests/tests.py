from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from ..models import *

from PIL import Image as ImageFile


def temporary_image():
    bts = BytesIO()
    img = ImageFile.new("RGB", (100, 100))
    img.save(bts, 'jpeg')
    return SimpleUploadedFile("test.jpg", bts.getvalue())


class CreateImagesTests(APITestCase):
    API_URL = '/create'

    def setUp(self):
        self.client = APIClient()
        my_admin = User.objects.create_superuser('admin', 'myemail@test.com', 'admin')
        self.client.force_authenticate(my_admin)

    def test_authenticated_user_image_is_created(self):
        """POST Attachments: Attachment is created."""
        image = temporary_image()

        data = {'description': 'DabApps', 'image': image}
        response = self.client.post(self.API_URL, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_non_authenticated_user_image_is_created(self):
        self.client.logout()
        image = temporary_image()

        data = {'description': 'DabApps', 'image': image}
        response = self.client.post(self.API_URL, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
