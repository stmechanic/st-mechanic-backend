from rest_framework import serializers


class GarageSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    specialty = ArrayField(serializers.CharField)
    username = None
    email = serializers.EmailField(unique=True, max_length=254)
    registration_number = serializers.CharField(max_length=20, unique=True)
    physical_address = serializers.CharField(
        max_length=255, blank=True, null=True)
    verified = serializers.BooleanField(default=False)
    opening_time = serializers.TimeField()
    closing_time = serializers.TimeField()
