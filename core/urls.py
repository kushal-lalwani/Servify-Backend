from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'users', UserProfileViewSet)
router.register(r'service-categories', ServiceCategoryViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('signup/user/', UserSignupView.as_view(), name='user-signup'),
    path('signup/employee/', EmployeeSignupView.as_view(), name='employee-signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('home/', HomePageAPIView.as_view(), name='home-page-api'),
    path('', include(router.urls)),
]
