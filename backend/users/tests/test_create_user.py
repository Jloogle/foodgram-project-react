from rest_framework import status
from rest_framework.test import APITestCase

from users.models import CustomUser


class UserTests(APITestCase):
    def test_create_user(self):
        """тест создания юзера"""
        url = 'http://127.0.0.1:8000/api/users/'
        data = {
            'email': 'lora@lora.ru',
            'username': 'LoraFirst',
            'password': '123Qwerty321',
            'first_name': 'Lora',
            'last_name': 'Snider',
            }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.get().username, 'LoraFirst')

