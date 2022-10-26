from django.test import TestCase

from accounts.forms import RegisterForm
from accounts.models import Account
from django.urls import reverse


class UserCreationFormTest(TestCase):
    def setUp(self):
        self.username = "testuser"
        self.email = "testuser@email.com"
        self.password = ("mypassword",)
        self.first_name = ("Kevin",)
        self.last_name = ("Sambulli",)
        self.address = ("address",)
        self.location = ("POINT (35.24414062009406 2.108898658949751)",)
        self.phone = ("0729759124",)

    def test_signup_page_url(self):
        response = self.client.get("/accounts/register/")
        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, template_name='account/register.html')

    def test_signup_page_view_name(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, template_name='account/register.html')

    def test_signup_form(self):
        data = {
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "address": self.address,
            "phone": self.phone,
            "location": self.location,
            "password1": self.password,
            "password2": self.password,
        }

        response = self.client.post(reverse("register"), data=data)
        self.assertEqual(response.status_code, 200)

        users = Account.objects.all()
        self.assertEqual(users.count(), 1)

    def test_renegistration_form_field_label(self):
        form = RegisterForm()
        self.assertTrue(
            form.fields["email"].label is None or form.fields["email"].label == ""
        )
        self.assertTrue(
            form.fields["phone"].label is None or form.fields["phone"].label == ""
        )
        self.assertTrue(
            form.fields["username"].label is None or form.fields["username"].label == ""
        )
        self.assertTrue(
            form.fields["first_name"].label is None
            or form.fields["first_name"].label == ""
        )
        self.assertTrue(
            form.fields["last_name"].label is None
            or form.fields["last_name"].label == ""
        )
        self.assertTrue(
            form.fields["address"].label is None or form.fields["address"].label == ""
        )
