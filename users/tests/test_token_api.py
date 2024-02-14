from users.tests.test_base import BaseAPITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse

class TokenRefreshViewTestCase(BaseAPITestCase):
    def test_refresh_token_success(self):
        url = reverse('token_refresh')  # Assuming the token refresh endpoint name is 'token_refresh'
        data = {'refresh': self.refresh_token}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_refresh_token_invalid(self):
        url = reverse('token_refresh')  # Assuming the token refresh endpoint name is 'token_refresh'
        data = {'refresh': 'invalid_refresh_token'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)