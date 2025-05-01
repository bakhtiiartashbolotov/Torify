from rest_framework import serializers
from .models import Tour

class TourSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "id",
            "tour_operator",
            "title",
            "description",
            "photo",
            "tour_date",
            "price",
            "status",
            "created_at",
            "updated_at",
        )
        model = Tour