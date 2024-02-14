from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken

class BaseAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='old_password')
        self.token = str(AccessToken.for_user(self.user))

    def tearDown(self):
        self.user.delete()