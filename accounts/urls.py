from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import (
    CustomUserLoginView, 
    CustomUserRegistrationView,
    update_profile, 
    profile, 
    UserProfileView, 
    activate_account, 
    update_password
)
from rest_framework_simplejwt.views import TokenObtainPairView

app_name = 'accounts'

urlpatterns = [
    # Authentication URLs
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),  # Django's built-in login
    path('logout/', LogoutView.as_view(), name='logout'),  # Django's built-in logout

    # Profile management
    path('profile/', profile, name='profile'),  # Function-based view for profile display
    path('profile/update/', update_profile, name='update_profile'),  # Function-based view for updating profile

    # API Endpoints
    path('api/register/', CustomUserRegistrationView.as_view(), name='api_register'),  # User registration API
    path('api/login/', CustomUserLoginView.as_view(), name='api_login'),  # User login API
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT token obtain endpoint
    path('api/profile/', UserProfileView.as_view(), name='api_profile'),  # User profile retrieval API
    path('activate/<uidb64>/<token>/', activate_account, name='activate'),  # Account activation endpoint
    path('api/update-password/', update_password, name='update_password'),  # Password update endpoint
]
