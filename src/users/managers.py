from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password

from src.users.user_constants import Role


class UserManager(BaseUserManager):
    def _create_user(self, email: str, password: str, **extra_fields):
        """Create and save a user with passed parameters."""

        email = self.normalize_email(email)
        password = make_password(password)
        user = self.model(email=email, password=password, **extra_fields)
        user.save()

        return user

    def create_user(self, email: str, password: str, **extra_fields):
        extra_fields["is_staff"] = False
        extra_fields["role"] = Role.USER

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str, **extra_fields):
        extra_fields["is_staff"] = True
        extra_fields["is_superuser"] = True
        extra_fields["role"] = Role.ADMIN

        return self._create_user(email, password, **extra_fields)