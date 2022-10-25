# Create your tests here.
from django.contrib.auth import get_user_model
from django.test import TestCase


class UsersManagersTests(TestCase):
    def setUp(self):
        pass
        # User = get_user_model()
        # self.user = User.objects.create_user(email='normal@user.com', username='kevin', first_name='Kevin',
        #                                      last_name='Samuli', password='myPass')

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email="normal@user.com",
            username="kevin",
            first_name="Kevin",
            last_name="Samuli",
            password="myPass",
            location="POINT (35.24414062009406 2.108898658949751)",
            address="address",
            phone="0729759023",
        )
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, "normal@user.com")
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email="",
                password="myPass",
                username="kevin",
                first_name="Kevin",
                last_name="Samuli",
                location="POINT (35.24414062009406 2.108898658949751)",
                address="address",
                phone="0729759023",
            )

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email="super@user.com",
            password="myPass",
            username="keviin",
            first_name="Kevoin",
            last_name="Samulli",
        )
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="super@user.com", password="foo", is_superuser=False
            )
