import re

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Company, JobSeeker


class RegisterCompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = [
            "email",
            "company_name",
            "nip_number",
            "password"
        ]

    def validate(self, attrs):
        """
        Verify email is valid and available
        """
        if re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", attrs["email"]) is None:
            raise ValidationError("email is invalid")
        if Company.objects.filter(email=attrs["email"]).exists() \
                or JobSeeker.objects.filter(email=attrs["email"]).exists():
            raise ValidationError("email is taken")

        """
        Verify nip_number is valid
        """
        if re.match(r"^\d{10}$", attrs["nip_number"]) is None:
            raise ValidationError("nip number is invalid")

        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.get("password")
        company = super().create(validated_data)
        company.set_password(password)
        company.save()

        return company



