from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = None
    id = models.AutoField(primary_key=True)
    full_name = models.CharField("Full Name", max_length=255)
    phone_number = models.CharField("Phone Number", max_length=15, unique=True)
    email = models.EmailField("Email", unique=True)
    role = models.CharField("Role", max_length=50,
                            choices=[("touroperator", "TourOperator"), ("user", "User")],
                            default="user")

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['role', 'full_name']