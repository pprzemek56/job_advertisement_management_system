from django.urls import path

from . import views

urlpatterns = [
    path("register_company/", views.company_create_view, name="register_company"),
    path("register_jobseeker/", views.job_seeker_create_view, name="register_job_seeker"),
    path("login/", views.login_view, name="log_in"),
]
