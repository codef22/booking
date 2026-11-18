from django.urls import path

from booking.views import (
    HealthCheckAPIView,
    ServicesListApiView,
    ServiceDetailAPIView,
    ServiceSummaryAPIView,
)

urlpatterns = [
    path("health/", HealthCheckAPIView.as_view(), name="api-health"),
    path("services/summary/", ServiceSummaryAPIView.as_view(), name="service-summary"),
    path("services/", ServicesListApiView.as_view(), name="service-list"),
    path("services/<int:pk>/", ServiceDetailAPIView.as_view(), name="service-detail"),
]