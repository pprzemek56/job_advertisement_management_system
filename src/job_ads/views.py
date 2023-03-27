from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics
from rest_framework import mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import JobOffer, Position
from .permissions import IsCompanyUser
from .serializers import JobOfferSerializer

from accounts.models import Company
from accounts.backend import AuthenticationBackend


class JobOfferListCreateView(
    generics.GenericAPIView,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
):
    """
        view for creating new job offer by company
    """
    authentication_classes = [AuthenticationBackend]
    serializer_class = JobOfferSerializer
    queryset = JobOffer.objects.all()

    def get_permissions(self):
        if self.request.method == "GET":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsCompanyUser]

        return [permission() for permission in permission_classes]

    def get(self, request: Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = self.request.user
        print(user)
        company = Company.objects.get(user_id=user.id)
        serializer.save(company=company)
        return super().perform_create(serializer)

    def create(self, request, *args, **kwargs):
        position_name = str(request.data.get("position")).strip().title()
        industry_name = str(request.data.get("industry")).strip().title()

        try:
            position = Position.objects.get(name=position_name)
        except ObjectDoesNotExist:
            position = Position.objects.create(name=position_name)
            position.save()

        request.data["position"] = position

        try:
            industry = Position.objects.get(name=industry_name)
        except ObjectDoesNotExist:
            industry = Position.objects.create(name=industry_name)
            industry.save()

        request.data["industry"] = industry

        return super().create(request, *args, **kwargs)


job_offer_list_create_view = JobOfferListCreateView().as_view()
