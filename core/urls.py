from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'users', UserProfileViewSet)
router.register(r'service-categories', ServiceCategoryViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('signup/user/', UserSignupView.as_view(), name='user-signup'),
    path('signup/employee/', EmployeeSignupView.as_view(), name='employee-signup'),
    path('employee/dashboard/', EmployeeDashboardView.as_view(), name='employee-dashboard'),
    path('place-order/', PlaceOrderView.as_view(), name='place-order'),
    path('employee/accept-order/<int:booking_id>/', AcceptOrderView.as_view(), name='accept-order'),
    path('employee/mark-completed/<int:booking_id>/', MarkOrderCompletedView.as_view(), name='mark-completed'),
    path('list-service-categories/', ServiceCategoryListView.as_view(), name='service-category-list'),
    path('login/', LoginView.as_view(), name='login'),
    path('home/', HomePageAPIView.as_view(), name='home-page-api'),
    path('', include(router.urls)),
]
