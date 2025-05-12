# tours/views.py
from rest_framework import generics, permissions, filters, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Tour, Booking
from .serializers import (
    TourSerializer, BookingSerializer, BookingManagementSerializer
)
from .permissions import IsTourOperator, IsBookingOwner, IsTourOperatorForBooking
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q

class TourViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Tours with different permissions based on action and role.
    """
    serializer_class = TourSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'tour_date', 'price']
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'tour_date', 'created_at']
    
    def get_queryset(self):
        queryset = Tour.objects.all()
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        if date_from:
            queryset = queryset.filter(tour_date__gte=date_from)
        if date_to:
            queryset = queryset.filter(tour_date__lte=date_to)
            
        # Additional filter for tour operators to see only their tours
        if self.request.user.is_authenticated and self.request.user.role == 'touroperator' and self.action in ['list', 'my_tours']:
            if self.action == 'my_tours':
                return queryset.filter(tour_operator=self.request.user)
        
        # For non-authenticated users, show only registration status tours
        if not self.request.user.is_authenticated:
            return queryset.filter(status='registration')
            
        return queryset
    
    def get_permissions(self):
        """
        Custom permissions:
        - Everyone can list and retrieve tours
        - Only tour operators can create, update, partial_update, and delete tours
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsTourOperator()]
        elif self.action in ['my_tours']:
            return [permissions.IsAuthenticated(), IsTourOperator()]
        elif self.action in ['bookings']:
            return [permissions.IsAuthenticated(), IsTourOperator()]
        return [permissions.AllowAny()]
    
    @action(detail=False, methods=['get'])
    def my_tours(self, request):
        """Get all tours created by the current tour operator."""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def bookings(self, request, pk=None):
        """Get all bookings for a specific tour."""
        tour = self.get_object()
        
        # Ensure the user is the tour operator for this tour
        if tour.tour_operator != request.user:
            return Response({'detail': 'You do not have permission to view these bookings.'},
                            status=status.HTTP_403_FORBIDDEN)
        
        bookings = Booking.objects.filter(tour=tour)
        serializer = BookingManagementSerializer(bookings, many=True)
        return Response(serializer.data)

class BookingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Bookings with different permissions based on action and role.
    """
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Regular users can see only their bookings
        if self.request.user.role == 'user':
            return Booking.objects.filter(user=self.request.user)
        
        # Tour operators can see bookings for their tours
        elif self.request.user.role == 'touroperator':
            return Booking.objects.filter(tour__tour_operator=self.request.user)
        
        return Booking.objects.none()
    
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'approve', 'decline']:
            return [permissions.IsAuthenticated(), IsTourOperatorForBooking()]
        elif self.action == 'destroy':
            # Allow both the booking owner and tour operator to cancel bookings
            return [permissions.IsAuthenticated(), (IsBookingOwner() | IsTourOperatorForBooking())]
        return [permissions.IsAuthenticated()]
    
    def get_serializer_class(self):
        if self.request.user.role == 'touroperator':
            return BookingManagementSerializer
        return BookingSerializer
    
    def perform_create(self, serializer):
        tour = serializer.validated_data['tour']
        
        # Check if the tour is open for registration
        if tour.status != 'registration':
            raise serializers.ValidationError({'detail': 'This tour is not available for booking.'})
        
        # Check if the tour date is in the future
        if tour.tour_date < timezone.now().date():
            raise serializers.ValidationError({'detail': 'This tour date has passed.'})
        
        # Check if the user already has a booking for this tour
        existing_booking = Booking.objects.filter(tour=tour, user=self.request.user).exists()
        if existing_booking:
            raise serializers.ValidationError({'detail': 'You already have a booking for this tour.'})
        
        serializer.save(user=self.request.user, status='pending')
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve a booking."""
        booking = self.get_object()
        booking.status = 'approved'
        booking.save()
        serializer = self.get_serializer(booking)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def decline(self, request, pk=None):
        """Decline a booking."""
        booking = self.get_object()
        booking.status = 'declined'
        booking.save()
        serializer = self.get_serializer(booking)
        return Response(serializer.data)

class TourOperatorBookingListView(generics.ListAPIView):
    """
    List all bookings for the tours created by the current tour operator.
    """
    serializer_class = BookingManagementSerializer
    permission_classes = [permissions.IsAuthenticated, IsTourOperator]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'tour']
    ordering_fields = ['created_at']
    
    def get_queryset(self):
        return Booking.objects.filter(tour__tour_operator=self.request.user)