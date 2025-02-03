from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ..models import MyUser, RefreshToken
from django.utils.timezone import now
from datetime import timedelta
from constance import config
from ..views import generate_access_token

class UserTests(APITestCase):
    def setUp(self):
        self.user = MyUser.objects.create_user(email='test@example.com', password='password123')
        self.login_url = reverse('login')
        self.register_url = reverse('register')
        self.profile_url = reverse('profile')
        self.refresh_url = reverse('refresh')
        self.access_token = generate_access_token(self.user)

    def test_register_user(self):
        data = {
            'email': 'newuser@example.com',
            'password': 'newpassword123'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MyUser.objects.count(), 2)

    def test_login_user(self):
        data = {
            'email': 'test@example.com',
            'password': 'password123'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)

    def test_profile_view(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test@example.com')

    def test_update_profile(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        data = {
            'username': 'updateduser'
        }
        response = self.client.put(self.profile_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'updateduser')
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')

    def test_refresh_token(self):
        refresh_token = RefreshToken.objects.create(
            user=self.user,
            expires_at=now() + timedelta(days=int(config.REFRESH_TOKEN_LIFETIME))
        )
        data = {
            'refresh_token': str(refresh_token.token)
        }
        response = self.client.post(self.refresh_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)