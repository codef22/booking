from rest_framework import serializers

from booking.models import ServiceOffering


class ServiceOfferingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceOffering
        fields = [
            "id",
            "title",
            "description",
            "duration_minutes",
            "price",
            "is_active"
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

    # اعتبارسنجی قیمت
    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "price can't be negetive."
            )

        return value
    
    # اعتبارسنجی مدت زمان خدمت
    def validate_duration_minutes(self, value):
        if value <15 or value >180:
            raise serializers.ValidationError(
                "duration must be between 15 min and 180 min"
            )

        return value

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

   