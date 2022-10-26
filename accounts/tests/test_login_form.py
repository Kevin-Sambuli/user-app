from django.test import TestCase

from accounts.models import Account


class LogInTest(TestCase):
    def setUp(self):
        self.credentials = {
            "username": "testuser",
            "password": "secret",
            "username": "testuser",
            "email": "testuser@email.com",
            "password": "mypassword",
            "first_name": "Kevin",
            "last_name": "Sambulli",
            "address": "address",
            "location": "POINT (35.24414062009406 2.108898658949751)",
            "phone": "0729759124",
        }
        Account.objects.create_user(**self.credentials)

    def test_login(self):
        # the text function test if the login form returns a positive response if a user passes  the right credentials
        data = {
            "email": "testuser@email.com",
            "password": "mypassword",
        }
        # send login data
        response = self.client.post("/accounts/login/", data, follow=True)
        print(response)

        # The user should be logged in now
        self.assertTrue(response.status_code, 200)
