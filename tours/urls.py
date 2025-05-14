from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TourViewSet, BookingViewSet

router = DefaultRouter()
router.register(r'tour', TourViewSet, basename='tour')
router.register(r'tour/bookings', BookingViewSet, basename='booking')

urlpatterns = [
    path('api/v1/', include(router.urls)),
]