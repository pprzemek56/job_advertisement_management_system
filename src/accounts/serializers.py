import re

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Company, JobSeeker, User


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

        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.get("password")
        user = super().create(validated_data)
        user.set_password(password)

        user.save()

        return user


class CompanySerializer(serializers.ModelSerializer):
    user = UserSerializer()

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
        user_data = validated_data.pop("user")
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        company = Company.objects.create(
            user=user,
            company_name=validated_data.pop("company_name"),
            nip_number=validated_data.pop("nip_number")
        )

        return company


class JobSeekerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

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
        user_data = validated_data.pop("user")
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        job_seeker = JobSeeker.objects.create(
            user=user,
            first_name=validated_data.pop("first_name"),
            last_name=validated_data.pop("last_name"),
            phone_number=validated_data.pop("phone_number"),
            cv=validated_data.pop("cv")
        )

        return job_seeker
