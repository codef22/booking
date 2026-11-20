from rest_framework import status, generics, mixins
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


class ServicesListApiView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView
):
    serializer_class = ServiceOfferingSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return ServiceOffering.objects.filter(is_active=True).order_by("id")

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ServicesListV2ApiView(
    generics.ListCreateAPIView
):
    serializer_class = ServiceOfferingSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return ServiceOffering.objects.filter(is_active=True).order_by("id")


class ServiceDetailAPIView(APIView):
    permission_classes = [AllowAny]


    def get_object(self, pk):
        return get_object_or_404(
            ServiceOffering,
            pk=pk,
            is_active=True,
        )


    def get(self, request, pk):
        service = self.get_object(pk)
        
        serializer = ServiceOfferingSerializer(service)

        return Response(serializer.data)

    def put(self, request, pk):
        service = self.get_object(pk)

        serializer = ServiceOfferingSerializer(
            service,
            data=request.data,
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def patch(self, request, pk):
        service = self.get_object(pk)

        serializer = ServiceOfferingSerializer(
            service,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, pk):
        service = self.get_object(pk)

        service.is_active = False

        service.save(update_fields=["is_active"])

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


class ServiceDetailV2APIView(generics.RetrieveUpdateAPIView):
    queryset = ServiceOffering.objects.filter(
        is_active=True
    )

    serializer_class = ServiceOfferingSerializer
    permission_classes = [AllowAny]

class ServiceDetailV3APIView(
    mixins.DestroyModelMixin,
    generics.RetrieveUpdateAPIView
):

    queryset = ServiceOffering.objects.filter(is_active=True)
    serializer_class = ServiceOfferingSerializer
    permission_classes = [AllowAny]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save(update_fields=["is_active"])

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class ServiceDeleteAPIView(APIView):

    permission_classes = [AllowAny]

    def delete(self, request, pk):
        service = get_object_or_404(
            ServiceOffering,
            pk=pk,
            is_active=True
        )

        service.is_active = False
        service.save(update_fields=["is_active"])

        return Response(status=status.HTTP_204_NO_CONTENT)