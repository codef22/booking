from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from django.shortcuts import get_object_or_404

from booking.models import ServiceOffering
from booking.serializers import ServiceOfferingSerializer


class HealthCheckAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            "status": "ok",
            "service": "smart-booking"
        })


class ServicesListApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        services = ServiceOffering.objects.filter(is_active=True).order_by("id")
        
        serializer = ServiceOfferingSerializer(services, many=True)

        return Response(serializer.data)


class ServiceDetailAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        service = get_object_or_404(
            ServiceOffering,
            pk=pk, is_active=True
        )
        
        serializer = ServiceOfferingSerializer(service)

        return Response(serializer.data)
