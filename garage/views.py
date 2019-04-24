from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Customer
from .serializers import CustomerSerializer, CustomerVerifySerializer
from .utils import send_mail

 
class CustomerCreateViewSet(viewsets.ModelViewSet):
    """
    API View that receives a POST with the following fields:
        - email
        - date of birth
        - national id
    Returns a one-time password that can be used for authenticated requests..
    """

    queryset = Customer.objects.all().order_by('-date_joined')
    serializer_class = CustomerSerializer
    permission_classes = (AllowAny,)

    @staticmethod
    def send_one_time_password(user):
        name = user.first_name
        password = user.national_id
        email_to = user.email
        verify_url = 'https://st-mechanic-dev'
        subject = 'Please verify your account'
        email_from = 'noreply@st-mechanic.com'
        content = ''
        return send_mail(
            email_to=email_to,
            email_from=email_from,
            content=content,
            subject=subject
        )

    def create(self, request):
        email = request.data.get('email')
        date_of_birth = request.data.get('date_of_birth')
        national_id = request.data.get('national_id')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            garage_user = Customer.objects.create_user(
                email=email,
                date_of_birth=date_of_birth,
                national_id=national_id,
                first_name=first_name,
                last_name=last_name
            )
            if garage_user:  # send one-time password to user
                self.send_one_time_password(user=garage_user)

            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        else:
            return Response({'error':
                             serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)




