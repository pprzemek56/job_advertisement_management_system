from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, status
from rest_framework import mixins
from rest_framework.request import Request
from rest_framework.response import Response

from .models import JobOffer, Position, Industry, JobApplication
from . import permissions
from . import serializers

from accounts.models import Company

from accounts.models import JobSeeker


class JobOfferListCreateView(
    generics.GenericAPIView,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
):
    """
        view for creating new job offer by company
    """
    serializer_class = serializers.JobOfferSerializer
    permission_classes = [permissions.IsCompanyOrReadOnly]
    queryset = JobOffer.objects.all()

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


class JobOfferRetrieveUpdateDeleteView(
    generics.GenericAPIView,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin
):
    serializer_class = serializers.JobOfferSerializer
    permission_classes = [permissions.CompanyOwnerOrReadOnly]
    queryset = JobOffer.objects.all()

    def get(self, request: Request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request: Request, *args, **kwargs):
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

        return self.update(request, *args, **kwargs)

    def delete(self, request: Request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


job_offer_retrieve_update_delete_view = JobOfferRetrieveUpdateDeleteView().as_view()


class JobApplicationListCreateView(
    generics.GenericAPIView,
    mixins.ListModelMixin,
    mixins.CreateModelMixin
):
    serializer_class = serializers.JobApplicationSerializer
    permission_classes = [permissions.IsJobSeekerOrReadOnly]
    queryset = JobApplication.objects.all()

    def get(self, request: Request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = self.request.user
        job_seeker = JobSeeker.objects.get(user_id=user.id)
        serializer.save(job_seeker=job_seeker)
        return super().perform_create(serializer)

    def post(self, request: Request, *args, **kwargs):
        print(request.FILES)

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            self.perform_create(serializer)
            serializer.save()

            response = {
                "message": "Job application created successfully",
                "data": serializer.data
            }

            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




job_application_list_create_view = JobApplicationListCreateView.as_view()
