from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, status
from rest_framework import mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import JobOffer, Position, Industry
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
        company = Company.objects.get(user_id=user.id)
        serializer.save(company=company)
        return super().perform_create(serializer)

    def post(self, request, *args, **kwargs):
        position_name = str(request.data.get("position")).strip().title()
        industry_name = str(request.data.get("industry")).strip().title()

        try:
            position = Position.objects.get(name=position_name)
        except ObjectDoesNotExist:
            position = Position.objects.create(name=position_name)
            position.save()

        request.data["position"] = position.pk

        try:
            industry = Industry.objects.get(name=industry_name)
        except ObjectDoesNotExist:
            industry = Industry.objects.create(name=industry_name)
            industry.save()

        request.data["industry"] = industry.pk

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            serializer.save()
            response = {
                "message": "Job offer created successfully",
                "data": serializer.data
            }

            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


job_offer_list_create_view = JobOfferListCreateView().as_view()
