# tweets/tests_accounts/test_tweets.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from tweets.models import Tweet

User = get_user_model()

class TweetTests(APITestCase):
    def setUp(self):
        # Cria um usuário de teste e autentica-o
        self.user = User.objects.create_user(
            username='@usuario',
            email='usuario@example.com',
            password='senha123'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_tweet(self):
        url = reverse('tweet-list-create')  # Ajuste conforme seu urls.py
        data = {"content": "Meu primeiro tweet!"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Tweet.objects.count(), 1)
        tweet = Tweet.objects.first()
        self.assertEqual(tweet.author, self.user)
        self.assertEqual(tweet.content, "Meu primeiro tweet!")

    def test_list_user_tweets(self):
        # Cria alguns tweets
        Tweet.objects.create(author=self.user, content="Tweet 1")
        Tweet.objects.create(author=self.user, content="Tweet 2")

        # Endpoint que lista os tweets do usuário autenticado
        url = reverse('tweet-list-user')  # Ajuste conforme seu urls.py
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Se estiver usando paginação, o resultado pode vir em response.data["results"]
        self.assertEqual(len(response.data["results"]), 2)
