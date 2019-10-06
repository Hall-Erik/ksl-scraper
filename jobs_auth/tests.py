from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient


class LogoutViewTests(TestCase):
    def test_auth_token_reset_on_logout(self):
        '''Logout should reset the auth token'''
        client = APIClient()
        user = User.objects.create_user(
            username='test', email='test@example.com', password='test123')
        url = reverse('jobs_auth:login')
        data = {
            'username': 'test',
            'password': 'test123'}
        # login to get key
        response = client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('key' in response.data)
        key = response.data['key']
        # logout
        client.force_authenticate(user=user)
        response = client.post(reverse('jobs_auth:logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # login again
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('key' in response.data)
        self.assertNotEqual(response.data['key'], key)


class LoginViewTests(TestCase):
    def test_login_works(self):
        '''
        Login should return a token key if good creds. given
        '''
        User.objects.create_user(
            username='test', email='test@example.com', password='test123')
        url = reverse('jobs_auth:login')
        data = {
            'username': 'test',
            'password': 'test123'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('key' in response.data)

    def test_cannot_login_with_bad_creds(self):
        '''
        Login should fail if given wrong password
        '''
        User.objects.create_user(
            username='test', email='test@example.com', password='test123')
        url = reverse('jobs_auth:login')
        data = {
            'username': 'test',
            'password': 'wrongPwd111'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('key' not in response.data)


class RegisterUserViewTests(TestCase):
    def test_register_user(self):
        '''Register endpoint should create a user'''
        url = reverse('jobs_auth:register')
        data = {
            'username': 'test',
            'email': 'test@example.com',
            'password1': 'testtest123',
            'password2': 'testtest123'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'test')


class CurrentUserViewTests(TestCase):
    def test_anon_user_cannot_access(self):
        '''Should return a 403 if not logged in'''
        response = self.client.get(reverse('jobs_auth:user_details'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_access(self):
        '''Logged in users can GET'''
        user = User.objects.create_user(
            username='test', email='test@example.com', password='test123')
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(reverse('jobs_auth:user_details'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
