from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Tour, Booking
from .serializers import (
    TourSerializer, BookingSerializer, BookingManagementSerializer
)
from .permissions import (
    IsTourOperator, IsBookingOwner, IsTourOperatorForBooking
)

class TourViewSet(viewsets.ModelViewSet):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        if self.action in ('create','update','partial_update','destroy'):
            return [permissions.IsAuthenticated(), IsTourOperator()]
        return super().get_permissions()

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated, IsTourOperator])
    def bookings(self, request, pk=None):
        tour = self.get_object()
        if tour.tour_operator != request.user:
            return Response({'detail':'Нет прав'}, status=status.HTTP_403_FORBIDDEN)
        qs = Booking.objects.filter(tour=tour)
        serializer = BookingManagementSerializer(qs, many=True)
        return Response(serializer.data)


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'touroperator':
            return Booking.objects.filter(tour__tour_operator=user)
        return Booking.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save()

class TourOperatorBookingListView(generics.ListAPIView):
    serializer_class = BookingManagementSerializer
    permission_classes = [permissions.IsAuthenticated, IsTourOperator]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'tour']
    ordering_fields = ['created_at']

    def get_queryset(self):
        return Booking.objects.filter(tour__tour_operator=self.request.user)