from users.tests.test_base import BaseAPITestCase
from rest_framework import status
from django.urls import reverse
from users.apis.serializers import ChangePasswordSerializer
from users.models import User

class ChangePasswordViewTestCase(BaseAPITestCase):
    def test_change_password_success(self):
        url = reverse('change_password')  # Assuming the change password endpoint name is 'change_password'
        data = {
            'old_password': 'password123',
            'new_password1': 'new_password',
            'new_password2': 'new_password'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get(username='test_user').check_password('new_password'), True)

    def test_change_password_invalid_old_password(self):
        url = reverse('change_password')  # Assuming the change password endpoint name is 'change_password'
        data = {
            'old_password': 'wrong_password',
            'new_password1': 'new_password',
            'new_password2': 'new_password'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('message', response.data)


    def test_change_password_mismatched_new_passwords(self):
        url = reverse('change_password')  # Assuming the change password endpoint name is 'change_password'
        data = {
            'old_password': 'password123',
            'new_password1': 'new_password1',
            'new_password2': 'new_password2'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Password is not matched.')


    def test_change_password_same_old_and_new_password(self):
        url = reverse('change_password')  # Assuming the change password endpoint name is 'change_password'
        data = {
            'old_password': 'password123',
            'new_password1': 'password123',
            'new_password2': 'password123'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Old and new password are same.')