from rest_framework import serializers
from .models import Tour, Booking
from django.contrib.auth import get_user_model

User = get_user_model()

class TourOperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'full_name', 'phone_number', 'email')

class TourSerializer(serializers.ModelSerializer):
    tour_operator_details = TourOperatorSerializer(source='tour_operator', read_only=True)
    booking_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Tour
        fields = (
            "id",
            "tour_operator",
            "tour_operator_details",
            "title",
            "description",
            "photo",
            "tour_date",
            "price",
            "status",
            "created_at",
            "updated_at",
            "booking_count",
        )
        read_only_fields = ('created_at', 'updated_at', 'tour_operator_details', 'booking_count')
        
    def get_booking_count(self, obj):
        return obj.bookings.count()
    
    def create(self, validated_data):
        validated_data['tour_operator'] = self.context['request'].user
        return super().create(validated_data)

class BookingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    tour = serializers.StringRelatedField(read_only=True)
    tour_id = serializers.PrimaryKeyRelatedField(queryset=Tour.objects.all(), source='tour', write_only=True)
    tour_details = TourSerializer(source='tour', read_only=True)
    
    class Meta:
        model = Booking
        fields = ('id', 'tour', 'tour_id', 'tour_details', 'user', 'status', 'created_at')
        read_only_fields = ('user', 'status', 'tour', 'created_at', 'tour_details')

class BookingManagementSerializer(serializers.ModelSerializer):
    user_details = serializers.SerializerMethodField(read_only=True)
    tour_details = TourSerializer(source='tour', read_only=True)
    
    class Meta:
        model = Booking
        fields = ('id', 'tour', 'user', 'user_details', 'tour_details', 'status', 'created_at')
        read_only_fields = ('tour', 'user', 'created_at', 'tour_details', 'user_details')
    
    def get_user_details(self, obj):
        return {
            'id': obj.user.id,
            'full_name': obj.user.full_name,
            'phone_number': obj.user.phone_number,
            'email': obj.user.email
        }