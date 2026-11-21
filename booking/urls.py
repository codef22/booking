from django.urls import path

from rest_framework.routers import DefaultRouter

from booking.views import (
    ServiceOfferingViewSet,
)

router = DefaultRouter()

router.register(
    r"services",
    ServiceOfferingViewSet,
    basename="service"
)

urlpatterns = router.urls

# urlpatterns = [
#     path("health/", HealthCheckAPIView.as_view(), name="api-health"),
#     # path("services/", ServicesListApiView.as_view(), name="service-list"),
#     # path("services2/", ServicesListV2ApiView.as_view(), name="service-list2"),
#     # path("services/<int:pk>/", ServiceDetailAPIView.as_view(), name="service-detail"),
#     # path("services2/<int:pk>/", ServiceDetailV2APIView.as_view(), name="service-detail2"),
# ]