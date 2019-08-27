"""API Serializers."""
from rest_framework import serializers
from .models import Garage, Vehicle, Job, Rating, Quote, Mechanic


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


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'


class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = '__all__'


class MechanicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mechanic
        fields = '__all__'
