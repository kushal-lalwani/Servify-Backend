from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import *
from .serializers import *

from django.contrib.auth import get_user_model
User = get_user_model()


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ServiceCategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer


class ServiceViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


class UserSignupView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        address = data.get('address')

        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        if UserProfile.objects.filter(user__username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name,
                                        last_name=last_name)
        UserProfile.objects.create(user=user, address=address, is_employee=False)

        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)


class EmployeeSignupView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        address = data.get('address')
        service_ids = data.get('services')
        is_employee = data.get('is_employee', True)

        if not username or not password or not email or not service_ids:
            return Response({'error': 'Username, password, email, and services are required'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        # Create user
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()

        # Create UserProfile
        user_profile = UserProfile.objects.create(
            user=user,
            address=address,
            is_employee=is_employee
        )
        user_profile.save()

        # Create Employee
        employee = Employee.objects.create(
            profile=user_profile,
            address=address,
            is_available=True
        )

        services = Service.objects.filter(id__in=service_ids)
        if not services.exists():
            return Response({'error': 'One or more services not found'}, status=status.HTTP_400_BAD_REQUEST)

        employee.services.set(services)
        employee.save()

        return Response({'message': 'Employee created successfully'}, status=status.HTTP_201_CREATED)




class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user_profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User profile does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': user.id,
            'email': user.email,
            'username': user.username,
            'is_employee': user_profile.is_employee
        }, status=status.HTTP_200_OK)


class HomePageAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        categories = ServiceCategory.objects.all()
        category_data = ServiceCategorySerializer(categories, many=True).data
        
        response_data = {
            'categories': [
                {'name': category['name'], 'image_url': category['image_url']}
                for category in category_data
            ]
        }
        for category in category_data:
            response_data[category['name']] = category['services']
        
        return Response(response_data)