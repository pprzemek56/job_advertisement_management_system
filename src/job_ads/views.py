from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics
from rest_framework import mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request

from .models import JobOffer, Position
from .permissions import IsCompanyUser
from .serializers import JobOfferSerializer


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

    permission_classes = [AllowAny]

    def get(self, request: Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    permission_classes = [IsCompanyUser]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(company=user)
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
