"""Garage API."""
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Garage
from .serializers import GarageSerializer


class GarageCreateViewSet(viewsets.ModelViewSet):
    """
    API View that receives a POST with a user's username and password.
    Returns a JSON Web Token that can be used for authenticated requests..
    """

    queryset = Garage.objects.all().order_by('-date_joined')
    serializer_class = GarageSerializer
    permission_classes = (AllowAny,)

    def create(self, request):
        data = request.data
        username, email = data.get('username'), data.get('email')
        password, confirm_password = data.get('password'),\
            data.get('confirm_password')
        if password == confirm_password:
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                User.objects.create_user(username=username, password=password,
                                         email=email)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            else:
                return Response({'error':
                                 'The email was not valid.'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'The passwords do not match'},
                            status=status.HTTP_400_BAD_REQUEST)
