from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from django.urls import reverse
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from common import utils

class ResetPasswordViewTestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(username='admin_user', email='admin@example.com', password='admin_password')
        self.user = User.objects.create_user(username='test_user', password='password123')
        self.token = str(AccessToken.for_user(self.admin_user))
        self.client.force_authenticate(user=self.admin_user)

    # def test_reset_password_success(self):
    #     url = reverse('reset_password')  # Assuming the reset password endpoint name is 'reset_password'
    #     user_id = utils.encode(self.user.id)  # Encode the user ID
    #     print(self.user.id,user_id)
    #     data = {
    #         'user_id': user_id,
    #         'new_password1': 'new_password',
    #         'new_password2': 'new_password'
    #     }
    #     response = self.client.post(url, data, format='json')

    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertTrue(User.objects.get(username='test_user').check_password('new_password'))

    def test_reset_password_invalid_user(self):
        url = reverse('reset_password')  # Assuming the reset password endpoint name is 'reset_password'
        invalid_user_id = 'invalid_user_id'
        data = {
            'user_id': invalid_user_id,
            'new_password1': 'new_password',
            'new_password2': 'new_password'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Something went wrong.")

    def test_reset_password_mismatched_new_passwords(self):
        url = reverse('reset_password')  # Assuming the reset password endpoint name is 'reset_password'
        user_id = utils.encode(self.user.id)  # Encode the user ID
        data = {
            'user_id': user_id,
            'new_password1': 'new_password1',
            'new_password2': 'new_password2'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Password must match. Please update your password.')

    def tearDown(self):
        self.admin_user.delete()
        self.user.delete()
