from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from django.shortcuts import get_object_or_404

from booking.models import ServiceOffering
from booking.serializers import (
    ServiceOfferingSerializer,
    ServiceSummarySerializer,
)

from django.db.models import Q
from rest_framework import status


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

        #search
        search = request.query_params.get("search")

        if search:
            services = services.filter(
                title__icontains=search
            )

        # Max Duration
        max_duration = request.query_params.get("max_duration")

        if max_duration is not None:
            try:
                max_duration = int(max_duration)

                if max_duration < 0:
                    return Response(
                        {"error": "max_duration must be a non-negative integer."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            except (ValueError, TypeError):
                return Response(
                    {"error": "max_duration must be a valid integer."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            services = services.filter(
                duration_minutes__lte=max_duration
            )
        
        serializer = ServiceOfferingSerializer(services, many=True)

        return Response(serializer.data)


class ServiceDetailAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        service = get_object_or_404(
            ServiceOffering,
            pk=pk, 
            is_active=True
        )
        
        serializer = ServiceOfferingSerializer(service)

        return Response(serializer.data)

class ServiceSummaryAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        services = ServiceOffering.objects.filter(
            is_active=True
        ).order_by("id")

        serializer = ServiceSummarySerializer(
            services,
            many=True
        )

        return Response(serializer.data)