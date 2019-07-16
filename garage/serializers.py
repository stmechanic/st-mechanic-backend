"""API Serializers."""
from rest_framework import serializers
from .models import Garage


class GarageSerializer(serializers.ModelSerializer):
    """Serialize Garage instances."""
    class Meta:
        model = Garage
        # fields = ('') 
