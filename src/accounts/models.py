from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class JobSeeker(AbstractBaseUser):
    """
    Single app user
    """
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=9, null=True, unique=True)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"


class Company(AbstractBaseUser):
    """
    Company app user
    """
    company_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    nip_number = models.CharField(max_length=13, unique=True)

    USERNAME_FIELD = "email"
