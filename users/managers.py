# users/managers.py

from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    """
    Менеджер пользователей, который использует phone_number вместо username.
    """

    use_in_migrations = True

    def create_user(self, phone_number, password=None, **extra_fields):
        """
        Создаёт и сохраняет обычного пользователя с заданным телефонным номером и паролем.
        """
        if not phone_number:
            raise ValueError(_('The Phone Number must be set'))
        # Нормализуем если нужно (например, убираем пробелы)
        phone_number = self.model.normalize_username(phone_number)
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        """
        Создаёт суперпользователя с правами staff и superuser.
        """
        extra_fields.setdefault('role', 'touroperator')        # или любой ролевой админ
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(phone_number, password, **extra_fields)