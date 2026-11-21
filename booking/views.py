from rest_framework import status, generics, mixins
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
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


class ServiceOfferingViewSet(ModelViewSet):
    # queryset = ServiceOffering.objects.filter(
    #     is_active=True
    # )

    # serializer_class = ServiceOfferingSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = ServiceOffering.objects.all()

        if self.action in ["list", "retrieve", "activate"]:
            return queryset

        return queryset.filter(is_active=True)

    def get_serializer_class(self):
        print("Current action:", self.action)
        return ServiceOfferingSerializer

    def perform_create(self, serializer):
        print("Creating service...")
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed("DELETE")

    @action(
        detail=True,
        methods=["post"],
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
    #activate
    @action(
        detail=True,
        methods=["post"],
        url_path="activate"
    )
    def activate(self, request, pk=None):
        service = self.get_object()

        service.is_active = True
        service.save(update_fields=["is_active"])

        return Response(
            {"message": "Serivice activated."},
            status=status.HTTP_200_OK
        )
    #shomaresh khadamat faal
    @action(
        detail=False,
        methods=["get"],
        url_path="active-count"
    )
    def active_count(self, request):
        count = ServiceOffering.objects.filter(
        is_active=True
        ).count()

        return Response(
            {"active_services": count},
            status=status.HTTP_200_OK
        )

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
