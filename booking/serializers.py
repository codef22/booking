from rest_framework import serializers


class ServiceOfferingSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    title = serializers.CharField()

    description = serializers.CharField()

    duration_minutes = serializers.IntegerField()

    price = serializers.IntegerField()

    is_active = serializers.BooleanField()

class ServiceSummarySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    title = serializers.CharField()
    
    duration_minutes = serializers.IntegerField()

