from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager as BUM
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class BaseUserManager(BUM):
    def create_user(self, phone_number, is_active=True, is_admin=False, password=None):
        if not phone_number:
            raise ValueError("Users must have a phone_number")

        user = self.model(
            phone_number=phone_number,
            is_active=is_active,
            is_admin=is_admin,
        )

        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.full_clean()
        user.save(using=self._db)

        return user

    def create_superuser(self, phone_number, password=None):
        user = self.create_user(
            phone_number=phone_number,
            is_active=True,
            is_staff=True,
            is_admin=True,
            password=password,
        )

        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(unique=True, max_length=11)
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = BaseUserManager()

    USERNAME_FIELD = "phone_number"

    def __str__(self):
        return self.phone_number

    class Meta:
        db_table = "User"
