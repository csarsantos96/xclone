# accounts/tests_accounts/test_accounts.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.core import signing

User = get_user_model()

class AccountTests(APITestCase):
    def test_user_registration_and_activation(self):
        """
        Testa fluxo de registro de usuário (is_active=False)
        e ativação via token.
        """
        # 1) Registrar usuário
        url = reverse('user-register')  # Ajuste conforme seu urls.py
        data = {
            "username": "@teste",
            "email": "teste@example.com",
            "password": "senha123",
            "first_name": "Teste",
            "last_name": "Usuario"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verifica que o usuário foi criado com is_active=False
        user = User.objects.get(username='@teste')
        self.assertFalse(user.is_active)

        # 2) Ativação do usuário
        token = signing.dumps({"user_id": user.id})
        activate_url = reverse('user-activate', kwargs={'token': token})
        # Fazemos GET para o endpoint de ativação
        response = self.client.get(activate_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user.refresh_from_db()
        self.assertTrue(user.is_active)
