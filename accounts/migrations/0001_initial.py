# Generated by Django 3.2.3 on 2022-10-28 18:26

import accounts.manager
import django.contrib.gis.db.models.fields
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Account",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "first_name",
                    models.CharField(max_length=30, verbose_name="First Name"),
                ),
                (
                    "last_name",
                    models.CharField(max_length=30, verbose_name="Last Name"),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=100, unique=True, verbose_name="Email"
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        max_length=30, null=True, unique=True, verbose_name="Username"
                    ),
                ),
                (
                    "address",
                    models.CharField(
                        blank=True, max_length=30, null=True, verbose_name="Address"
                    ),
                ),
                (
                    "phone",
                    models.CharField(
                        blank=True,
                        max_length=10,
                        null=True,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="phone number should exactly be in 10 digits",
                                regex="^\\d{10}$",
                            )
                        ],
                        verbose_name="Phone",
                    ),
                ),
                (
                    "location",
                    django.contrib.gis.db.models.fields.PointField(
                        blank=True, null=True, srid=4326, verbose_name="Location"
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(auto_now_add=True, verbose_name="Date Joined"),
                ),
                (
                    "last_login",
                    models.DateTimeField(auto_now=True, verbose_name="last login"),
                ),
                ("is_admin", models.BooleanField(default=False, verbose_name="admin")),
                (
                    "is_active",
                    models.BooleanField(default=False, verbose_name="active"),
                ),
                ("is_staff", models.BooleanField(default=True, verbose_name="staff")),
                (
                    "is_superuser",
                    models.BooleanField(default=False, verbose_name="superuser"),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "Accounts",
                "verbose_name_plural": "Accounts",
                "db_table": "accounts",
            },
            managers=[
                ("objects", accounts.manager.UserManager()),
            ],
        ),
    ]
