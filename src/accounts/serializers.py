import re

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Company, JobSeeker, User


class CompanyWithUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=20, write_only=True)
    is_company_user = serializers.BooleanField(default=True)
    company_name = serializers.CharField(max_length=255)
    nip_number = serializers.CharField(max_length=10)

    def validate_email(self, value):
        if re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", value) is None:
            raise ValidationError("email is invalid")
        if User.objects.filter(email=value).exists():
            raise ValidationError("email is taken")

        return value

    def validate_nip_number(self, value):
        if re.match(r"^\d{10}$", value) is None:
            raise serializers.ValidationError("nip number is invalid")
        if Company.objects.filter(nip_number=value).exists():
            raise serializers.ValidationError("nip number is taken")
        return value

    def create(self, validated_data):
        user_data = {
            "email": validated_data.pop("email"),
            "password": validated_data.pop("password"),
            "is_company_user": validated_data.pop("is_company_user")
        }

        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        company_data = {
            "user": user.id,
            "company_name": validated_data.pop("company_name"),
            "nip_number": validated_data.pop("nip_number")
        }

        company_serializer = CompanySerializer(data=company_data)
        company_serializer.is_valid(raise_exception=True)
        company = company_serializer.save()

        return company


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, max_length=20, write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "is_company_user"
        ]

    def validate(self, attrs):
        """
        Verify email is valid and available
        """
        if re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", attrs["email"]) is None:
            raise ValidationError("email is invalid")
        if User.objects.filter(email=attrs["email"]).exists():
            raise ValidationError("email is taken")

        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.get("password")
        user = super().create(validated_data)
        user.set_password(password)

        user.save()

        return user


class CompanySerializer(serializers.ModelSerializer):
    user = User()

    class Meta:
        model = Company
        fields = [
            "user",
            "company_name",
            "nip_number",
        ]

    def validate(self, attrs):
        """
        Verify nip_number is valid
        """
        if re.match(r"^\d{10}$", attrs["nip_number"]) is None:
            raise ValidationError("nip number is invalid")

        return super().validate(attrs)

    def create(self, validated_data):
        company = super().create(validated_data)
        company.save()

        return company


class JobSeekerSerializer(serializers.ModelSerializer):
    user = User()

    class Meta:
        model = JobSeeker
        fields = [
            "user",
            "first_name",
            "last_name",
            "phone_number",
            "cv",
        ]

    def validate(self, attrs):
        """
        Verify phone_number is valid
        """
        if re.match(r"^\d{9}$", attrs["phone_number"]) is None:
            raise ValidationError("phone number is invalid")

        """
        Verify first_name is valid
        """
        if re.match(r"^[a-zA-Z]+$", attrs["first_name"]) is None:
            raise ValidationError("first name is invalid")

        """
        Verify last_name is valid
        """
        if re.match(r"^[a-zA-Z]+$", attrs["last_name"]) is None:
            raise ValidationError("last name is invalid")

        return super().validate(attrs)

    def create(self, validated_data):
        job_seeker = super().create(validated_data)
        job_seeker.save()

        return job_seeker
