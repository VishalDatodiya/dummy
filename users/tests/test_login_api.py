from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .test_base import BaseAPITestCase
from django.urls import reverse

class LoginAPITestCase(BaseAPITestCase):
    def test_login_success(self):
        url = reverse('login')  # Assuming the login endpoint name is 'login'
        data = {
            'username': 'test_user',
            'password': 'password123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if 'token' key exists in response data
        self.assertIn('token', response.data)

        # Access 'token' key and then check for 'refresh'
        token_data = response.data.get('token', {})
        self.assertIn('refresh', token_data)
        self.assertIn('access', token_data)
        self.assertIn('access_time_limit', token_data)


    def test_login_failure(self):
        url = reverse('login')  # Assuming the login endpoint name is 'login'
        data = {
            'username': 'test_user',
            'password': 'wrong_password'  # Providing incorrect password
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('refresh', response.data)
        self.assertNotIn('access', response.data)
        self.assertNotIn('access_time_limit', response.data)
