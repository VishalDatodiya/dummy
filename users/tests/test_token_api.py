from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse

class TokenRefreshViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='password123')
        self.refresh_token = str(RefreshToken.for_user(self.user))
        self.client.force_authenticate(user=self.user)  # Authenticate the client

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

    def tearDown(self):
        self.user.delete()
