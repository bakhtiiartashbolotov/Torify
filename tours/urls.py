from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TourViewSet, BookingViewSet, TourOperatorBookingListView
)

router = DefaultRouter()
router.register(r'', TourViewSet, basename='tour')
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = [
    path('', include(router.urls)),
    path('bookings/operator/', TourOperatorBookingListView.as_view(), name='tour-operator-bookings'),
]