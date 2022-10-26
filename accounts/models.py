from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.gis.db import models as geoModels
from django.core.mail import send_mail
from django.core.serializers import serialize
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from accounts.manager import UserManager

from django.contrib.gis.geos import Point
from geopy.geocoders import Nominatim


class Account(AbstractBaseUser, PermissionsMixin):
    """This Class Model is used to create a custom User model by Overiding the django default User model.
    This allows to extend the User models with more fields.
    """

    first_name = models.CharField("First Name", max_length=30)
    last_name = models.CharField("Last Name", max_length=30)
    email = models.EmailField("Email", blank=False, max_length=100, unique=True)
    username = models.CharField("Username", max_length=30, unique=True)
    address = models.CharField("Address", max_length=30, blank=True)
    phone_regex = RegexValidator(
        regex=r"^\d{10}$", message="phone number should exactly be in 10 digits"
    )
    phone = models.CharField(
        "Phone",
        max_length=15,
        validators=[phone_regex],
        unique=True,
        blank=True,
        null=True,
    )
    location = geoModels.PointField("Location", blank=True, null=True, srid=4326)

    date_joined = models.DateTimeField("Date Joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)

    # permissions
    is_admin = models.BooleanField("admin", default=False)
    is_active = models.BooleanField("active", default=False)
    is_staff = models.BooleanField("staff", default=True)
    is_superuser = models.BooleanField("superuser", default=False)

    # unique parameter that will be used to login in the user
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "username"]

    # hooking the New customized Manager to our Model to allow us to perform actions on the model
    objects = UserManager()

    class Meta:
        db_table = "accounts"
        verbose_name = "Accounts"
        verbose_name_plural = "Accounts"

        # permissions = (
        #     ('view_account', 'view Account'),
        # )

    def __str__(self):
        """The string method returns the full names of the User instance"""
        return "{}".format(self.get_full_name())

    def save(self, *args, **kwargs):
        # geolocator = Nominatim(user_agent="location")
        # if self.address is not None:
        #     g = geolocator.geocode(self.address)
        #     self.location = Point(g.longitude, g.latitude)

        super().save(*args, **kwargs)
        # user_group, created = Group.objects.get_or_create(name='users')
        # staff_group, created = Group.objects.get_or_create(name='staff')
        # admin_group, created = Group.objects.get_or_create(name='admin')

    def get_full_name(self):
        """Returns the first_name plus the last_name, with a space in between."""
        full_name = "%s %s" % (self.first_name.title(), self.last_name.title())
        return full_name.strip()

    def email_user(self, subject, message):
        """The method when called is responsible for sending an email to this User instance.
        the sender is the django declared Default From Email in the setting.py"""
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [self.email],
            fail_silently=False,
        )

    @classmethod
    def getUserData(cls):
        """
        The class method allows to perform modal based operations.
        This class methods returns all Users from the database in geojson format to enable compatibility with
        leaflet GeoJSON
        """

        # users = serializers.serialize("json", Account.objects.all())
        # return HttpResponse(users, content_type="json")
        return serialize("geojson", cls.objects.all())


# @receiver(pre_save, sender=Account)
# def create_location(sender, instance, *args, **kwargs):
#     geolocator = Nominatim(user_agent="location")
#     if instance.address is not None:
#         g = geolocator.geocode(instance.address)
#         instance.location = Point(g.longitude, g.latitude)
