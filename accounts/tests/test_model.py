# Create your tests here.
from django.contrib.auth import get_user_model
from django.test import TestCase
from accounts.models import Account


class UsersManagersTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Account.objects.create_user(
            email="normal@user.com",
            username="kevon",
            first_name="Kevin",
            last_name="Samuli",
            password="myPass",
            location="POINT (35.24414062009406 2.108898658949751)",
            address="address",
            phone="0729759024",
        )

    def setUp(self):
        #  Get an author object to test
        self.user = Account.objects.get(id=1)

        self.admin_user = Account.objects.create_superuser(
            email="super@user.com",
            password="superuser",
            username="super",
            first_name="Kevin",
            last_name="Sambulli",
            location="POINT (35.24414062009406 2.108898658949751)",
            address="address",
            phone="0729759124",
        )

    def test_create_user(self):
        # the test the normal user creation in the database
        self.assertIsInstance(self.user, Account)
        # self.assertEqual(self.user.email, "normal@user.com")
        self.assertTrue(self.user.is_staff)
        self.assertFalse(self.user.is_active)
        self.assertFalse(self.user.is_superuser)

        with self.assertRaises(TypeError):
            Account.objects.create_user()
        with self.assertRaises(TypeError):
            Account.objects.create_user(email="")

    def test_create_superuser(self):
        self.assertEqual(self.admin_user.email, "super@user.com")
        self.assertTrue(self.admin_user.is_active)
        self.assertTrue(self.admin_user.is_staff)
        self.assertTrue(self.admin_user.is_superuser)

        # with self.assertRaises(ValueError):
        #     Account.objects.create_superuser(
        #         email="super@user.com",
        #         username="kevin",
        #         first_name="Kevin",
        #         last_name="Sambulli",
        #         password="superuser",
        #         is_superuser=False,
        #     )

    def test_first_name_label(self):
        # Get the metadata for the required field and use it to query the required field data
        field_label = self.user._meta.get_field("first_name").verbose_name
        self.assertEqual(field_label, "First Name")

    def test_first_name_max_length(self):
        # Get the metadata for the required field and use it to query the required field data
        max_length = self.user._meta.get_field("first_name").max_length
        self.assertEqual(max_length, 30)

    def test_object_name_is_first_name_comma_last_name(self):
        # tests the string method if returns the expected output
        expected_object_name = (
            f"{self.user.first_name.title()}{self.user.last_name.title()}"
        )
        self.assertEqual(str(self.user), expected_object_name)

    def test_object_phone_number_is_ten_digits(self):
        # tests the length of the user telephone number. it should return true if its 10 digits
        phone_number_length = self.user._meta.get_field("phone").max_length

        self.assertEqual(phone_number_length, 10)
