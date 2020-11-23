from django.urls import reverse
from django.test import override_settings
from rest_framework import status
from rest_framework.test import APITestCase

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
