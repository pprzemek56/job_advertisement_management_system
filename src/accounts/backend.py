from django.contrib.auth.backends import BaseBackend
from django.core.exceptions import ObjectDoesNotExist

from .models import Company, JobSeeker


class AuthenticationBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = Company.objects.get(email=email)
            print(email)
            print(password)
        except ObjectDoesNotExist:
            try:
                user = JobSeeker.objects.get(email=email)
            except ObjectDoesNotExist:
                return None

        if user.check_password(password):
            return user

        return None
