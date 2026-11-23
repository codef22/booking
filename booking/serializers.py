from rest_framework import serializers

from booking.models import (
    ServiceOffering,
    ProviderProfile,
    AvailabilitySlot
)


class ProviderProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        source="user.username",
        read_only=True,
    )

    class Meta:
        model = ProviderProfile
        fields = [
            "id",
            "username",
            "bio",
            "is_verified",
        ]


class ServiceOfferingSerializer(serializers.ModelSerializer):
    provider = serializers.PrimaryKeyRelatedField(
        queryset=ProviderProfile.objects.all(),
        allow_null=True,
        required=False,
    )

    class Meta:
        model = ServiceOffering
        fields = [
            "id",
            "title",
            "description",
            "duration_minutes",
            "price",
            "is_active",
            "provider"
        ]
        read_only_fields = [
            "id",
            "is_active"
        ]

    def validate_title(self, value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError(
                "Title must have at least 5 char."
            )

        return value.strip()

    def validate(self, attrs):
        duration = attrs.get("duration_minutes")
        price = attrs.get("price")

        if duration is not None and price is not None:
            if duration > 120 and price == 0:
                raise serializers.ValidationError({
                    "price": (
                        "Service longer than 120 minute cannot be free."
                    )
                })

        return attrs


class ServiceDetailSerializer(
    serializers.ModelSerializer
):
    provider = ProviderProfileSerializer(
        read_only=True
    )

    class Meta:
        model = ServiceOffering
        fields = [
            "id",
            "title",
            "description",
            "duration_minutes",
            "price",
            "is_active",
            "provider",
        ]



class ServiceSummarySerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = ServiceOffering
        fields = [
            "id",
            "title",
            "duration_minutes",
            "price",
        ]


class ProviderDetailSerializer(
    ProviderProfileSerializer
):
    services = ServiceSummarySerializer(
        many=True,
        read_only=True
    )

    class Meta(ProviderProfileSerializer.Meta):
        fields = (
            ProviderProfileSerializer.Meta.fields
            + ["services"]
        )



class AvailabilitySlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailabilitySlot
        fields = [
            "id",
            "provider",
            "start_at",
            "end_at",
            "is_active",
        ]
        read_only_fields = ["id"]

    def validate(self, attrs):
        start = attrs.get(
            "start_at",
            getattr(self.instance, "start_at", None)
        )
        end = attrs.get(
            "end_at",
            getattr(self.instance, "end_at", None)
        )

        if start is not None and end is not None:
            if end <= start:
                raise serializers.ValidationError({
                    "end_at": "End time must be after start time."
                })

        return attrs