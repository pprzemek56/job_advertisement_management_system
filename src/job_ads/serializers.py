from rest_framework.serializers import ModelSerializer

from .models import Position, Industry, JobOffer


class PositionSerializer(ModelSerializer):
    class Meta:
        model = Position
        fields = [
            "id",
            "name"
        ]


class IndustrySerializer(ModelSerializer):
    class Meta:
        model = Industry
        fields = [
            "id",
            "name"
        ]


class JobOfferSerializer(ModelSerializer):
    class Meta:
        model = JobOffer
        fields = [
            "id",
            "company",
            "title",
            "description",
            "contract_type",
            "working_type",
            "position",
            "industry",
            "month_salary"
        ]
