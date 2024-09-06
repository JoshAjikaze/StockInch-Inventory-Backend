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
from .forms import UserProfileForm
from .serializers import UserProfileSerializer


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



@method_decorator(csrf_exempt, name='dispatch')
class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user



class UserProfileView(generics.RetrieveAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user



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



@login_required
def profile(request):
    return JsonResponse({
        "user": CustomUserSerializer(request.user).data
    }, status=status.HTTP_200_OK)
