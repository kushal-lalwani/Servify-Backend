# core/serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Employee, Service, ServiceCategory, Booking

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'address', 'is_employee']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'profile']

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user, **profile_data)
        return user

class EmployeeSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = Employee
        fields = ['profile', 'services', 'is_available', 'address']

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create_user(**profile_data)
        profile = UserProfile.objects.create(user=user, **profile_data)
        employee = Employee.objects.create(profile=profile, **validated_data)
        return employee

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'category', 'name', 'description', 'price']

class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ['id', 'name', 'description']

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'user', 'service', 'employee', 'date', 'status']

