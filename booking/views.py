from rest_framework import status, generics, mixins
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

from booking.models import (
    ServiceOffering,
    ProviderProfile,
    AvailabilitySlot,
)
from booking.serializers import (
    ServiceOfferingSerializer,
    ServiceDetailSerializer,
    ProviderProfileSerializer,
    ProviderDetailSerializer,
    AvailabilitySlotSerializer,
)


class HealthCheckAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            "status": "ok",
            "service": "smart-booking"
        })


class ServiceOfferingViewSet(ModelViewSet):
    # queryset = ServiceOffering.objects.filter(
    #     is_active=True
    # )

    # serializer_class = ServiceOfferingSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = ServiceOffering.objects.all()

        if self.action in ["list", "retrieve"]:
            return queryset

        return queryset.filter(is_active=True)

    def get_serializer_class(self):
        print("Current action:", self.action)
        if self.action == "retrieve":
            return ServiceDetailSerializer

        return ServiceOfferingSerializer

    def perform_create(self, serializer):
        print("Creating service...")
        provider = serializer.validated_data.get("provider")

        print("provider:", provider)
        print("provider type:", type(provider))

        serializer.save()

    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed("DELETE")

    @action(
        detail=True,
        methods=["get"],
        url_path="deactivate"
    )
    def deactivate(self, request, pk=None):
        service = self.get_object()

        service.is_active = False
        service.save(update_fields=["is_active"])

        return Response(
            {"message": "Serivice deactivated."},
            status=status.HTTP_200_OK
        )


class ProviderViewSet(ReadOnlyModelViewSet):
    permission_classes = [AllowAny]

    queryset = ProviderProfile.objects.all()

    def get_queryset(self):
        return ProviderProfile.objects.select_related(
            "user"
        ).prefetch_related(
            "services"
        )

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProviderDetailSerializer

        return ProviderProfileSerializer


class AvailabilitySlotViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = AvailabilitySlotSerializer

    queryset = AvailabilitySlot.objects.all()

    # def get_queryset(self):
    #     return AvailabilitySlot.objects.select_related(
    #         "provider"
    #     ).order_by("start_at")
    def get_queryset(self):

        queryset = AvailabilitySlot.objects.select_related(
            "provider"
        ).order_by("start_at")

        provider_id = self.request.query_params.get("provider_id")

        if provider_id is not None:

            if not provider_id.isdigit():
                 raise ValidationError({
                    "provider_id": "Provider ID must be a number."
                })

            queryset = queryset.filter(
                provider_id=provider_id
            )

        return queryset


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


class ServiceDetailV2APIView(generics.RetrieveUpdateAPIView):
    queryset = ServiceOffering.objects.filter(
        is_active=True
    )

    serializer_class = ServiceOfferingSerializer
    permission_classes = [AllowAny]
