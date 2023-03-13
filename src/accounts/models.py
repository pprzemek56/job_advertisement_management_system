from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class JobSeekerManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, first_name, last_name, phone_number, password, **extra_fields):
        # TODO: refactor raise exception
        values = [email, first_name, last_name]
        for value in values:
            if not value:
                raise ValueError("The given {} must be set".format())
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, first_name, last_name, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, first_name, last_name, phone_number, password, **extra_fields)


class JobSeeker(AbstractBaseUser):
    """
    Single app user
    """
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=9, null=True, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # TODO: add cv field

    objects = JobSeekerManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".title().strip()

    def get_short_name(self):
        return f"{self.first_name}".title().strip()


class CompanyManager(BaseUserManager):
    # use_in_migrations = True
    #
    # def _create_user(self, email, company_name, nip_number):
    #     if
    pass


class Company(AbstractBaseUser):
    """
    Company app user
    """
    email = models.EmailField(unique=True)
    company_name = models.CharField(max_length=200)
    nip_number = models.CharField(max_length=13, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return f"{self.company_name} {self.nip_number}".title().strip()

    def get_short_name(self):
        return f"{self.company_name}".title().strip()
