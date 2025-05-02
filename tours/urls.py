from django.urls import path
from .views import TourList, TourDetail, BookingListCreateView, BookingDetailView

urlpatterns = [
    path("<int:pk>/", TourDetail.as_view(), name="tour-detail"),
    path("", TourList.as_view(), name="tour-list"),
    path("bookings/", BookingListCreateView.as_view(), name="booking-list-create"),
    path("bookings/<int:pk>/", BookingDetailView.as_view(), name="booking-detail"),
]