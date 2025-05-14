from rest_framework import viewsets, permissions, filters, status, generics
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

from .models import Tour, Booking
from .serializers import (
    TourSerializer,
    BookingSerializer,
    BookingManagementSerializer,
)
from .permissions import (
    IsTourOperator,
    IsBookingOwner,
    IsTourOperatorForBooking,
)


class TourViewSet(viewsets.ModelViewSet):

    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ['status', 'tour_date', 'price']
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'tour_date', 'created_at']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsTourOperator()]
        if self.action in ['my_tours', 'bookings']:
            return [permissions.IsAuthenticated(), IsTourOperator()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(tour_operator=self.request.user)

    @action(detail=False, methods=['get'])
    def my_tours(self, request):
        qs = Tour.objects.filter(tour_operator=request.user)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def bookings(self, request, pk=None):
        tour = self.get_object()
        if tour.tour_operator != request.user:
            return Response(
                {'detail': 'Нет прав просматривать бронирования.'},
                status=status.HTTP_403_FORBIDDEN
            )
        qs = Booking.objects.filter(tour=tour)
        serializer = BookingManagementSerializer(qs, many=True)
        return Response(serializer.data)


class BookingViewSet(viewsets.ModelViewSet):

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'tour']
    ordering_fields = ['created_at']

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Booking.objects.none()
        if user.role == 'user':
            return Booking.objects.filter(user=user)
        return Booking.objects.filter(tour__tour_operator=user)

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        if self.action in ['update', 'partial_update', 'approve', 'decline']:
            return [permissions.IsAuthenticated(), IsTourOperatorForBooking()]
        if self.action == 'destroy':
            return [permissions.IsAuthenticated(), (IsBookingOwner() | IsTourOperatorForBooking())]
        return [permissions.IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.user.role == 'touroperator':
            return BookingManagementSerializer
        return BookingSerializer

    def perform_create(self, serializer):
        tour = serializer.validated_data['tour']
        if tour.status != 'registration':
            raise serializers.ValidationError({'detail': 'Тур недоступен для бронирования.'})
        if tour.tour_date < timezone.now().date():
            raise serializers.ValidationError({'detail': 'Дата тура уже прошла.'})
        if Booking.objects.filter(tour=tour, user=self.request.user).exists():
            raise serializers.ValidationError({'detail': 'У вас уже есть бронирование.'})
        serializer.save(user=self.request.user, status='pending')

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        booking = self.get_object()
        booking.status = 'approved'
        booking.save()
        return Response(self.get_serializer(booking).data)

    @action(detail=True, methods=['post'])
    def decline(self, request, pk=None):
        booking = self.get_object()
        booking.status = 'declined'
        booking.save()
        return Response(self.get_serializer(booking).data)


class TourOperatorBookingListView(generics.ListAPIView):

    serializer_class = BookingManagementSerializer
    permission_classes = [permissions.IsAuthenticated, IsTourOperator]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'tour']
    ordering_fields = ['created_at']

    def get_queryset(self):
        return Booking.objects.filter(tour__tour_operator=self.request.user)