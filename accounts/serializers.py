from rest_framework import serializers
from accounts.models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'name', 'email', 'phone_number', 'password', 'role')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            name=validated_data['name'],
            email=validated_data['email'],
            phone_number=validated_data.get('phone_number', None),
            password=validated_data['password'],
            role=validated_data.get('role', 'shopper')  # Default is 'shopper' if role is not provided
        )
        return user
    


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['name', 'phone_number', 'email', 'address', 'profile_picture']
        read_only_fields = ['email']

