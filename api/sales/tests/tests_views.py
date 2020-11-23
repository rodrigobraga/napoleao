from unittest import mock

import responses

from django.urls import reverse
from django.test import override_settings
from rest_framework import status
from rest_framework.test import APITestCase

from django.conf import settings

from rest_framework_simplejwt.tokens import RefreshToken

from model_bakery import baker


@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class SaleTests(APITestCase):
    def setUp(self):
        self.user = baker.make_recipe(
            "users.user",
            email="foo@nbar.ai",
            first_name="Foo",
            last_name="Bar",
            cpf="33887264002"
        )

        refresh = RefreshToken.for_user(self.user)
        access_token = f"{refresh.access_token}"
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    def test_create(self):
        url = reverse('sales:sale-list')
        payload = {
            "code": "aUniqueCodeIdentifierFromReseler",
            "value": 1000.99,
            "date": "2020-11-10T12:00:00-03:00",
            "reseller": self.user.username
        }
        response = self.client.post(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list(self):
        baker.make_recipe("sales.sale", reseller=self.user, _quantity=3)
        url = reverse('sales:sale-list')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get(self):
        sale = baker.make_recipe("sales.sale", reseller=self.user)
        url = reverse('sales:sale-detail', args=[sale.identifier])
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update(self):
        sale = baker.make_recipe("sales.sale", reseller=self.user)
        url = reverse('sales:sale-detail', args=[sale.identifier])
        payload = {
            "code": "aUniqueCodeIdentifierFromReseler",
            "value": 10,
            "date": "2020-11-10T12:00:00-03:00",
            "reseller": self.user.username
        }
        response = self.client.put(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch(self):
        sale = baker.make_recipe("sales.sale", reseller=self.user)
        url = reverse('sales:sale-detail', args=[sale.identifier])
        payload = {
            "value": 50,
        }
        response = self.client.patch(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        sale = baker.make_recipe("sales.sale", reseller=self.user)
        url = reverse('sales:sale-detail', args=[sale.identifier])
        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @responses.activate
    def test_get_accumulated(self):
        responses.add(
            responses.GET,
            settings.ACCUMULATED_API_BASE_URL,
            json={
                "statusCode": 200,
                "body": {
                    "credit": 4467
                }
            },
            status=200
        )

        url = reverse('sales:sale-accumulated')
        data = {"cpf": self.user.cpf}

        response = self.client.get(url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"credit": 4467})

    @responses.activate
    def test_get_accumulated_error(self):
        responses.add(
            responses.GET,
            settings.ACCUMULATED_API_BASE_URL,
            json={
                "statusCode": 400,
                "body": {
                    "message": "error"
                }
            },
            status=200
        )

        url = reverse('sales:sale-accumulated', args=[])
        data = {"cpf": self.user.cpf}

        response = self.client.get(url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {"message": "error"})

    @mock.patch("sales.views.requests")
    def test_get_accumulated_unknown_error(self, m_requests):
        m_requests.get.side_effect = Exception("out")

        url = reverse('sales:sale-accumulated')
        data = {"cpf": self.user.cpf}

        response = self.client.get(url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
