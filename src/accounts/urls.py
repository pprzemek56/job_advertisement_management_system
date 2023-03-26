from django.urls import path

from . import views

urlpatterns = [
    path("register_company/", views.create_company, name="register_company"),
    path("register_jobseeker/", views.create_job_seeker, name="register_job_seeker"),
    path("login/", views.login_view, name="log_in"),
]
