from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(
        self,
        email,
        username,
        first_name,
        last_name,
        location=None,
        address=None,
        phone=None,
        password=None,
    ):
        if not email:
            raise ValueError("Please provide a valid email")
        if not username:
            raise ValueError("Please provide a username")
        if not first_name:
            raise ValueError("Provide your first Name")
        if not last_name:
            raise ValueError("Provide your last Name")
        # if not address:
        #     raise ValueError(" Please provide your home address")
        # if not phone:
        #     raise ValueError("Please provide your telephone number")

        email = self.normalize_email(email)
        email = email.lower()

        user = self.model(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            location=location,
            phone=phone,
            address=address,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email,
        first_name,
        last_name,
        username,
        password=None,
    ):
        user = self.create_user(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

