from django.urls import include, path
from django.contrib.auth.views import LoginView, LogoutView
from .views import CustomUserLoginView, CustomUserRegistrationView, update_profile, profile, UserProfileView
from rest_framework_simplejwt.views import TokenObtainPairView

app_name = 'accounts'

urlpatterns = [
    # Authentication URLs
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),  
    path('logout/', LogoutView.as_view(), name='logout'), 

    # Profile management (function-based views)
    path('profile/', profile, name='profile'),
    path('profile/update/', update_profile, name='update_profile'),

    # API Endpoints
    path('api/register/', CustomUserRegistrationView.as_view(), name='api_register'),  
    path('api/login/', CustomUserLoginView.as_view(), name='api_login'),  
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT token obtain endpoint
    path('api/profile/', UserProfileView.as_view(), name='api_profile'),  
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),
    path('api/update-password/', views.update_password, name='update_password'),
]
