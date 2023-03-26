from django.contrib import admin

from .models import JobSeeker, Company, User

admin.site.register(JobSeeker)
admin.site.register(Company)
admin.site.register(User)
