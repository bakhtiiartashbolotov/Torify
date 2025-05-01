from django.urls import path
from .views import TourList, TourDetail

urlpatterns = [
    path("<int:pk>/", TourDetail.as_view(), name="tour-detail"),
    path("", TourList.as_view(), name="tour-list"),
]