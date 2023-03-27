from django.db import models

from accounts.models import Company, JobSeeker


class Position(models.Model):
    name = models.CharField(max_length=50)


class Industry(models.Model):
    name = models.CharField(max_length=50)


CONTRACT_TYPES = (
    ("COE", "Umowa o pracę"),
    ("CW", "Umowa o dzieło"),
    ("MC", "Umowa zlecenie"),
    ("B2B", "Umowa B2B"),
    ("RC", "Umowa zastępstwa"),
    ("AA", "Umowa agencyjna"),
    ("TEC", "Umowa o pracę tymczasową"),
    ("IC", "Umowa stażowa")
)

WORKING_TYPES = (
    ("FT", "Pełny etat"),
    ("PT", "Praca na niepełny etat"),
    ("SJ", "Praca sezonowa")
)


class JobOffer(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=50)
    description = models.TextField()
    contract_type = models.CharField(max_length=50, choices=CONTRACT_TYPES)
    working_type = models.CharField(max_length=50, choices=WORKING_TYPES)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, blank=True)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE, null=True, blank=True)
    month_salary = models.IntegerField(default=None, null=True, blank=True)


class JobApplication(models.Model):
    job_seeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    message = models.TextField(null=True, blank=True)
    cv = models.FileField(upload_to="\\job_application_resumes")
