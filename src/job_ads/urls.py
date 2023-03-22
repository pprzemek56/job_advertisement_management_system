from django.urls import path

from .views import job_offer_list_create_view

urlpatterns = [
    path("", job_offer_list_create_view, name="list_create_job_offer")
]
