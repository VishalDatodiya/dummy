from rest_framework.test import APITestCase
from users.models import User
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.tokens import RefreshToken


class BaseAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='password123')
        self.token = str(AccessToken.for_user(self.user))
        self.refresh_token = str(RefreshToken.for_user(self.user))
        self.client.force_authenticate(user=self.user)

    def tearDown(self):
        self.user.delete()
