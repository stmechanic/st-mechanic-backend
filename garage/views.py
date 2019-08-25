"""Garage API."""
from django.db.utils import IntegrityError

from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Garage, Vehicle, Job, Rating
from .serializers import GarageSerializer, VehicleSerializer, JobSerializer, RatingSerializer, QuoteSerializer


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all().order_by('-date_created')
    serializer_class = JobSerializer
    permission_classes = (IsAuthenticated, )


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer


class RatingViewSet(viewsets.ModelViewSet):
    serializer_class = RatingSerializer
    permission_classes = (IsAuthenticated, )

    def list(self, request, *args, **kwargs):
        queryset = Rating.objects.filter(job__garage=request.user)
        serializer = RatingSerializer(queryset=queryset, many=True)
        return Response(serializer.data)


class QuoteViewSet(viewsets.ModelViewSet):
    serializer_class = QuoteSerializer
    permission_classes = (IsAuthenticated, )


class GarageCreateViewSet(viewsets.ModelViewSet):
    """
    API View that receives a POST with a user's username and password.
    Returns a JSON Web Token that can be used for authenticated requests..
    """

    queryset = Garage.objects.all().order_by('-date_joined')
    serializer_class = GarageSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        data = request.data
        name, email = data.get('name'), data.get('email')
        location = data.get('location')
        password, confirm_password = data.get('password1'),\
            data.get('password2')
        registration_number = data.get('registration_number')
        if password == confirm_password:
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                try:
                    Garage.objects.create_user(
                        name=name,
                        password=password,
                        location=location,
                        email=email,
                        registration_number=registration_number
                    )
                    return Response(serializer.data,
                                    status=status.HTTP_201_CREATED)
                except IntegrityError as exception:
                    return Response({'error': 'The Garage already exists'},
                                    status=status.HTTP_400_BAD_REQUEST)
            return Response({'error':
                            'The email was not valid.'},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'The passwords do not match'},
                        status=status.HTTP_400_BAD_REQUEST)
