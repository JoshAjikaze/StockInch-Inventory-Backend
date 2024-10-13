from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from accounts.models import CustomUser
from accounts.serializers import CustomUserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import update_session_auth_hash
from .forms import UserProfileForm
from .serializers import UserProfileSerializer

# Custom User Registration View
@method_decorator(csrf_exempt, name='dispatch')
class CustomUserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return JsonResponse({
            "user": CustomUserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User registered successfully."
        }, status=status.HTTP_201_CREATED)


class SignUpView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        return super().form_valid(form)
    
# Custom User Login View
@method_decorator(csrf_exempt, name='dispatch')
class CustomUserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = CustomUser.objects.filter(email=email).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return JsonResponse({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return JsonResponse({"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)


# User Profile Update View
@method_decorator(csrf_exempt, name='dispatch')
class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


# Profile View (Read-Only)
class UserProfileView(generics.RetrieveAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


# Update Profile Function-Based View (Can be Deprecated)
@csrf_exempt
@login_required
def update_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": "Profile updated successfully."}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "Invalid form submission"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        form = UserProfileForm(instance=user)
        return JsonResponse({"form": form}, status=status.HTTP_200_OK)


# Profile Function-Based View
@login_required
def profile(request):
    return JsonResponse({
        "user": CustomUserSerializer(request.user).data
    }, status=status.HTTP_200_OK)

#email verification view
def send_verification_email(request, user):
    current_site = get_current_site(request)
    subject = 'Activate Your Account'
    message = render_to_string('registration/activation_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    user.email_user(subject, message)
    

def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return JsonResponse({'message': 'Account activated successfully.'}, status=200)
    else:
        return JsonResponse({'error': 'Activation link is invalid.'}, status=400)
    
#Password update
@csrf_exempt
@login_required
def update_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password == confirm_password:
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)  # To prevent session invalidation
            return JsonResponse({'success': 'Password updated successfully.'}, status=200)
        else:
            return JsonResponse({'error': 'Passwords do not match.'}, status=400)
    return JsonResponse({'error': 'Invalid request method.'}, status=400)
