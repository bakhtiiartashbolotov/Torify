from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TourViewSet, BookingViewSet, TourOperatorBookingListView

router = DefaultRouter()

router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'', TourViewSet, basename='tour')

urlpatterns = [
    path('', include(router.urls)),
    path('bookings/operator/', TourOperatorBookingListView.as_view(), name='tour-operator-bookings'),
]