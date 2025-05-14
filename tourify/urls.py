from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from tours.views import TourViewSet, BookingViewSet, TourOperatorBookingListView

schema_view = get_schema_view(
    openapi.Info(
        title="Tourify API",
        default_version="v1",
        description="API documentation for Tourify",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@tourify.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)

router = DefaultRouter()
router.register(r'tour', TourViewSet, basename='tour')
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(router.urls)),
    path(
        "api/v1/bookings/operator/",
        TourOperatorBookingListView.as_view(), 
        name="tour-operator-bookings"
    ),
    path('api/v1/users/', include('users.urls')),
    path("docs/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
]