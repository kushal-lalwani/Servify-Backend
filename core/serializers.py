# core/serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    class Meta:
        model = UserProfile
        fields = ['user', 'address', 'is_employee']

    def get_user(self, obj):
        return {
            'username': obj.user.username,
            'email': obj.user.email,
            'first_name': obj.user.first_name,
            'last_name': obj.user.last_name,
        }

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
        fields = ['profile', 'service_categories', 'is_available', 'address']

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create_user(**profile_data)
        profile = UserProfile.objects.create(user=user, **profile_data)
        employee = Employee.objects.create(profile=profile, **validated_data)
        return employee

class ReviewSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    service = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    
    class Meta:
        model = Review
        fields = ['id', 'service', 'user', 'rating', 'comment', 'created_at']
        depth = 1  # This will show nested relationships (e.g., service name and user name)

    def get_created_at(self, obj):
        ist_time = obj.created_at.astimezone(pytz.timezone('Asia/Kolkata'))
        return ist_time.strftime("%Y-%m-%d %H:%M:%S")

class ServiceSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True, read_only=True)
    
    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'price', 'image_url', 'reviews']

    def get_image_url(self, obj):
        return obj.image.url if obj.image else None

class ServiceCategorySerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    services = ServiceSerializer(many=True, read_only=True)

    class Meta:
        model = ServiceCategory
        fields = ['id', 'name', 'services', 'image_url']
        
    def get_image_url(self, obj):
        return obj.image.url if obj.image else None

class BookingSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()


    class Meta:
        model = Booking
        fields = ['id', 'user', 'service', 'employee', 'date', 'status']

    def get_date(self, obj):
       ist_time = obj.date.astimezone(pytz.timezone('Asia/Kolkata'))
       return ist_time.strftime("%Y-%m-%d %H:%M:%S")



class PaymentSerializers(serializers.ModelSerializer):
    
    class Meta:
        model=Payment
        fields=['user','order_id',' payment_id','signature','amount','currency',' status','created_at']

