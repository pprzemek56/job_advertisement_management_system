from django.contrib import admin

from .models import Position, Industry, JobOffer, JobApplication

admin.site.register(Position)
admin.site.register(Industry)
admin.site.register(JobOffer)
admin.site.register(JobApplication)
