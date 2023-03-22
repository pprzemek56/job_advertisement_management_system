from rest_framework.serializers import ModelSerializer

from .models import Position, Industry


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
