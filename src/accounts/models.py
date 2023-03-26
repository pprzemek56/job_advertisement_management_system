from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        if not password:
            raise ValueError("The Password field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    is_company_user = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class JobSeekerManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, first_name, last_name, phone_number, **extra_fields):
        user = User.objects.get(email=email)
        values = [first_name, last_name]
        field_value_map = dict(zip(self.model.REQUIRED_FIELDS, values))
        for field_name, value in field_value_map:
            if not value:
                raise ValueError("The given {} must be set".format(field_name))
        job_seeker = self.model(
            user=user,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            **extra_fields
        )
        job_seeker.save(using=self._db)
        return job_seeker

    def create_user(self, email, first_name, last_name, phone_number, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, first_name, last_name, phone_number, **extra_fields)


class JobSeeker(AbstractBaseUser):
    """
    Single app user
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=9, null=True, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    cv = models.FileField(upload_to="\\resumes", null=True, blank=True)

    objects = JobSeekerManager()

    USERNAME_FIELD = "user"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.first_name

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".title().strip()

    def get_short_name(self):
        return f"{self.first_name}".title().strip()


class CompanyManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, company_name, nip_number, **extra_fields):
        user = User.objects.get(email=email)
        values = [company_name, nip_number]
        field_value_map = dict(zip(self.model.REQUIRED_FIELDS, values))
        for field_name, value in field_value_map:
            if not value:
                raise ValueError("The {} value must be set".format(field_name))
        company = self.model(
            user=user,
            company_name=company_name,
            nip_number=nip_number,
            **extra_fields
        )
        company.save(using=self._db)
        return company

    def create_user(self, email, company_name, nip_number, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, company_name, nip_number, **extra_fields)


class Company(AbstractBaseUser):
    """
    Company app user
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    nip_number = models.CharField(max_length=10, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CompanyManager()

    USERNAME_FIELD = "user"
    REQUIRED_FIELDS = ["company_name", "nip_number"]

    def __str__(self):
        return self.company_name

    def get_full_name(self):
        return f"{self.company_name} {self.nip_number}".title().strip()

    def get_short_name(self):
        return f"{self.company_name}".title().strip()
