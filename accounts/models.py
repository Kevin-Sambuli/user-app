from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.serializers import serialize
from django.core.validators import RegexValidator
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.gis.db import models as geoModels
from .manager import UserManager
from django.db import models


class Account(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField('First Name', max_length=30)
    last_name = models.CharField('Last Name', max_length=30)
    email = models.EmailField('Email', blank=False, max_length=100, unique=True)
    username = models.CharField('Username', max_length=30, unique=True)
    address = models.CharField('Address', max_length=100, blank=True)
    phone_regex = RegexValidator(regex=r'^\d{10}$', message="phone number should exactly be in 10 digits")
    phone = models.CharField('Phone', max_length=255, validators=[phone_regex], unique=True, blank=True, null=True)
    location = geoModels.PointField('Location', blank=True, null=True, srid=4326)

    date_joined = models.DateTimeField('Date Joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)

    # permissions
    is_admin = models.BooleanField('admin', default=False)
    is_active = models.BooleanField('active', default=False)
    is_staff = models.BooleanField('staff', default=False)
    is_superuser = models.BooleanField('superuser', default=False)

    # unique parameter that will be used to login in the user
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    # hooking the New customized Manager to our Model
    objects = UserManager()

    class Meta:
        db_table = 'accounts'
        verbose_name = "Accounts"
        verbose_name_plural = "Accounts"

    def __str__(self):
        return '{}'.format(self.get_full_name())

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_full_name(self):
        """ Returns the first_name plus the last_name, with a space in between. """
        full_name = '%s %s' % (self.first_name.title(), self.last_name.title())
        return full_name.strip()

    def email_user(self, subject, message):
        """Sends an email to this User. """
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [self.email], fail_silently=False)

    @classmethod
    def getUserData(cls):
        """ Returns the centroid of a specified parcel"""

        return serialize('geojson', cls.objects.all())
