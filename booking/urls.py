from django.urls import path

from booking.views import (
    HealthCheckAPIView,
    ServicesListApiView,
    ServicesListV2ApiView,
    ServiceDetailAPIView,
    ServiceDetailV2APIView,
    ServiceDetailV3APIView,
    ServiceDeleteAPIView,
)

urlpatterns = [
    path("health/", HealthCheckAPIView.as_view(), name="api-health"),
    path("services/", ServicesListApiView.as_view(), name="service-list"),
    path("services2/", ServicesListV2ApiView.as_view(), name="service-list2"),
    path("services/<int:pk>/", ServiceDetailAPIView.as_view(), name="service-detail"),
    path("services2/<int:pk>/", ServiceDetailV2APIView.as_view(), name="service-detail2"),
    path("services3/<int:pk>/", ServiceDetailV3APIView.as_view(), name="service-detail3"),
    path("services/<int:pk>/delete/", ServiceDeleteAPIView.as_view(), name="service-delete"),
]