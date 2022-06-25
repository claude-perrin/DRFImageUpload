from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.admin import User
from rest_framework.test import APILiveServerTestCase, APITestCase, APIClient

from backend.adapter.models import (
    Image, Profile, Tier, Thumbnail
)

"""
GET to view should give images and thumbnails appropriate to a user

Profiles with thumbnails should see appropriate thumbnails
Profiles with expiring links should be able to see binary expiring links
Profiles with original images should be able to see original images
"""


class CreateAttachmentTests(APITestCase):
    API_URL = '/create'

    def test_attachment_is_created(self):
        """POST Attachments: Attachment is created."""
        self.client = APIClient()
        my_admin = User.objects.create_superuser('admin', 'myemail@test.com', 'admin')
        self.client.force_authenticate(my_admin)
        with open('tests/newfolder.png') as fb:
            data = {'description': 'DabApps', 'image': None}
        response = self.client.post(self.API_URL, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


# class CreateAttachmentTests(APITestCase):
#     API_URL = '/create'
#
#     def test_attachment_is_created(self):
#         """POST Attachments: Attachment is created."""
#         client = APIClient()
#         my_admin = User.objects.create_superuser('admin', 'myemail@test.com', 'admin')
#
#
#         data = {'description': 'DabApps'}
#         response = self.client.post(self.API_URL, data, format='json')
#         self.assertEqual(response.status_code, 200)

# self.assertEqual(Account.objects.count(), 1)
# self.assertEqual(Account.objects.get().name, 'DabApps')
