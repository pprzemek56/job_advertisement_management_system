from django.urls import path

from . import views

urlpatterns = [
    path("", views.job_offer_list_create_view, name="list_create_job_offer"),
    path("<int:pk>/", views.job_offer_retrieve_update_delete_view, name="retrieve_update_delete_job_offer"),
]
