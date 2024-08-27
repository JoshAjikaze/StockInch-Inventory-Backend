from django.urls import include, path
from django.contrib.auth.views import LoginView, LogoutView
from .views import CustomUserLoginView, SignUpView, CustomUserRegistrationView, update_profile, profile, UserProfileView
from rest_framework_simplejwt.views import TokenObtainPairView
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('onboarding/', views.onboarding, name='onboarding'),
    path('promo/', views.promo, name='promo'),
    path('inventory/', include('inventory.urls')),
    path('profile/', profile, name='profile'),
    path('profile/update/', update_profile, name='update_profile'),

    # API endpoints
    path('api/register/', CustomUserRegistrationView.as_view(), name='api_register'),
    path('api/login/', CustomUserLoginView.as_view(), name='api_login'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/register/', CustomUserRegistrationView.as_view(), name='register'),
    path('api/login/', CustomUserLoginView.as_view(), name='login'),
    path('api/profile/', UserProfileView.as_view(), name='api_profile'),
]
