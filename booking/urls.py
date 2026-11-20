from django.urls import path

from booking.views import (
    HealthCheckAPIView,
    ServicesListApiView,
    ServicesListV2ApiView,
    ServiceDetailAPIView,
)

urlpatterns = [
    path("health/", HealthCheckAPIView.as_view(), name="api-health"),
    path("services/", ServicesListApiView.as_view(), name="service-list"),
    path("services2/", ServicesListV2ApiView.as_view(), name="service-list2"),
    path("services/<int:pk>/", ServiceDetailAPIView.as_view(), name="service-detail"),
]