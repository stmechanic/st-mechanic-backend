"""API Serializers."""
from rest_framework import serializers
from .models import Garage, Vehicle


class GarageSerializer(serializers.ModelSerializer):
    """Serialize Garage instances."""
    class Meta:
        model = Garage
        fields = ('name', 'email', 'registration_number')


class VehicleSerializer(serializers.ModelSerializer):
    """Serialize Vehicle instances"""
    class Meta:
        model = Vehicle
        fields = ('year', 'vin', 'make', 'model')
