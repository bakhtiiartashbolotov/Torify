from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import Tour, Booking

User = get_user_model()


class TourOperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'full_name', 'phone_number', 'email')


class TourSerializer(serializers.ModelSerializer):
    """
    Сериализатор туров с деталями оператора, лимитом участников и количеством бронирований.
    """
    tour_operator_details = TourOperatorSerializer(
        source='tour_operator', read_only=True
    )
    booking_count = serializers.SerializerMethodField()

    class Meta:
        model = Tour
        fields = (
            'id', 'tour_operator', 'tour_operator_details',
            'title', 'description', 'photo', 'tour_date', 'price',
            'status', 'max_participants', 'booking_count',
            'created_at', 'updated_at',
        )
        read_only_fields = (
            'id', 'tour_operator', 'tour_operator_details',
            'status', 'booking_count', 'created_at', 'updated_at',
        )
    def get_booking_count(self, obj):
        return obj.bookings.count()
    def create(self, validated_data):
        # Привязываем тур к текущему туроператору и открываем регистрацию
        validated_data['tour_operator'] = self.context['request'].user
        validated_data['status'] = 'registration'
        return super().create(validated_data)


class BookingSerializer(serializers.ModelSerializer):
    """
    Сериализатор бронирования: проверка лимита и возврат деталей пользователя и тура.
    """
    user_details = serializers.SerializerMethodField(read_only=True)
    tour_id = serializers.PrimaryKeyRelatedField(
        queryset=Tour.objects.filter(status='registration'),
        source='tour', write_only=True
    )
    tour_details = TourSerializer(source='tour', read_only=True)

    class Meta:
        model = Booking
        fields = (
            'id', 'tour_id', 'tour_details',
            'user_details', 'status', 'created_at'
        )
        read_only_fields = ('id', 'tour_details', 'user_details', 'status', 'created_at')

    def get_user_details(self, obj):
        return {
            'id': obj.user.id,
            'full_name': obj.user.full_name,
            'phone_number': obj.user.phone_number,
            'email': obj.user.email,
        }

    def validate(self, attrs):
        tour = attrs['tour']
        user = self.context['request'].user
        # Проверяем, что есть свободные места
        if tour.booking_count >= tour.max_participants:
            raise serializers.ValidationError({'detail': 'Мест больше нет.'})
        # Проверяем, что пользователь ещё не бронировал
        if Booking.objects.filter(tour=tour, user=user).exists():
            raise serializers.ValidationError({'detail': 'Вы уже бронировали этот тур.'})
        # Проверяем дату тура
        if tour.tour_date < timezone.now().date():
            raise serializers.ValidationError({'detail': 'Дата тура уже прошла.'})
        return attrs

    def create(self, validated_data):
        # Сохраняем бронь со статусом pending
        return Booking.objects.create(
            user=self.context['request'].user,
            **validated_data
        )


class BookingManagementSerializer(serializers.ModelSerializer):
    """
    Сериализатор для менеджмента бронирований туроператором.
    """
    user_details = serializers.SerializerMethodField(read_only=True)
    tour_details = TourSerializer(source='tour', read_only=True)

    class Meta:
        model = Booking
        fields = (
            'id', 'tour', 'user', 'user_details',
            'tour_details', 'status', 'created_at'
        )
        read_only_fields = fields

    def get_user_details(self, obj):
        return {
            'id': obj.user.id,
            'full_name': obj.user.full_name,
            'phone_number': obj.user.phone_number,
            'email': obj.user.email,
        }