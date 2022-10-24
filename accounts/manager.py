from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, username, first_name, last_name, password=None):
        if not email:
            raise ValueError('Please provide a valid email')
        if not username:
            raise ValueError('Please provide a username')
        if not first_name:
            raise ValueError('Provide your first Name')
        if not last_name:
            raise ValueError('Provide your last Name')

        email = self.normalize_email(email)
        email = email.lower()

        user = self.model(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, username, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        # user.Types.MANAGER
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


