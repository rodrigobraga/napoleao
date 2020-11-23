from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from rest_framework_simplejwt.tokens import RefreshToken

from model_bakery import baker


class AuthTests(APITestCase):
    def setUp(self):
        self.user = baker.make_recipe('users.user')
        self.user.set_password('secret')
        self.user.save()

    def test_obtain_pair(self):
        url = reverse('token_obtain_pair')
        payload = {
            'email': self.user.email,
            'password': 'secret'
        }
        response = self.client.post(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_token_refresh(self):
        url = reverse('token_refresh')
        
        refresh = RefreshToken.for_user(self.user)

        payload = {
            'refresh': str(refresh)
        }

        response = self.client.post(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_token_verify(self):
        url = reverse('token_verify')
        
        token = RefreshToken.for_user(self.user)

        payload = {
            'token': str(token)
        }

        response = self.client.post(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserTests(APITestCase):
    def setUp(self):
        self.user = baker.make_recipe('users.user')

        refresh = RefreshToken.for_user(self.user)
        access_token = f'{refresh.access_token}'
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    def test_create(self):
        url = reverse('users:register-list')
        payload = {
            'email': 'fulanoe@unknown.com',
            'first_name': 'Fulano',
            'last_name': 'Oliveira',
            'cpf': '16246276415',
            'password': '$3cR3T',
        }
        response = self.client.post(url, payload, format='json')

        payload.pop('password')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), payload)
    
    def test_update(self):
        url = reverse('users:user-detail', args=[self.user.username])
        payload = {
            'email': 'sicrano@unknown.ai',
            'first_name': 'Sicrano',
            'last_name': 'Tavares',
            'cpf': '33887264002',
        }
        response = self.client.put(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), payload)

    def test_patch(self):
        url = reverse('users:user-detail', args=[self.user.username])
        payload = {
            'first_name': 'Beltrano',
        }
        response = self.client.patch(url, payload, format='json')

        expected = {
            'email': self.user.email,
            'first_name': 'Beltrano',
            'last_name': self.user.last_name,
            'cpf': self.user.cpf,
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected)
