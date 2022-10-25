from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import Account


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_users_register(self):
        response = self.client.get(reverse('register'))

        self.assertEquals(response.status_code, 200)

        self.assertTemplateUsed(response, 'account/register')
