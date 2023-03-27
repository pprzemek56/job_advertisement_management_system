from django.contrib.auth.backends import BaseBackend
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from .models import User


class AuthenticationBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            return None

        if user.check_password(password):
            return user

        return None

    def authenticate_header(self, request):
        return 'Bearer realm="%s"' % _('api')
