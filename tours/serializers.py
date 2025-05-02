from rest_framework import serializers
from .models import Tour, Booking

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

class BookingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    tour = serializers.StringRelatedField(read_only=True)
    tour_id = serializers.PrimaryKeyRelatedField(queryset=Tour.objects.all(), source='tour', write_only=True)

    class Meta:
        model = Booking
        fields = ('id', 'tour', 'tour_id', 'user', 'status', 'created_at')
        read_only_fields = ('user', 'status', 'tour', 'created_at')