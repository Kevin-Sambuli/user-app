from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import Account


class TestViews(TestCase):
    def test_map_view_url_exists_at_desired_location(self):
        response = self.client.get("/accounts/map/")
        self.assertEqual(response.status_code, 200)

    def test_map_view_url_accessible_by_name(self):
        response = self.client.get(reverse("map"))
        self.assertEqual(response.status_code, 200)

    def test_login_view_url_exists_at_desired_location(self):
        response = self.client.get("/accounts/login/")
        self.assertEqual(response.status_code, 200)

    def test_login_view_url_accessible_by_name(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_register_view_url_exists_at_desired_location(self):
        response = self.client.get("/accounts/register/")
        self.assertEqual(response.status_code, 200)

    def test_register_view_url_accessible_by_name(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)

    def test_register_view_uses_correct_template(self):
        response = self.client.get(reverse("register"))
        self.assertTemplateUsed(response, "accounts/register.html")

    def test_login_view_uses_correct_template(self):
        response = self.client.get(reverse("login"))
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_map_view_uses_correct_template(self):
        response = self.client.get(reverse("map"))
        self.assertTemplateUsed(response, "map/webmap.html")
