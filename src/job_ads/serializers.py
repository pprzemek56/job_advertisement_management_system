from rest_framework.serializers import ModelSerializer

from .models import Position


class PositionSerializer(ModelSerializer):
    class Meta:
        model = Position
        fields = [
            "id",
            "name"
        ]


