from rest_framework import serializers
from accounts.models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    profile_picture_url = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('id', 'name', 'email', 'phone_number', 'password', 'role', 'address', 'profile_picture', 'profile_picture_url')

    def get_profile_picture_url(self, obj):
        request = self.context.get('request')
        if obj.profile_picture and hasattr(obj.profile_picture, 'url'):
            return request.build_absolute_uri(obj.profile_picture.url)
        return None

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            name=validated_data['name'],
            email=validated_data['email'],
            phone_number=validated_data.get('phone_number', None),
            password=validated_data['password'],
            role=validated_data.get('role', 'shopper'),
            address=validated_data.get('address', ''),
            profile_picture=validated_data.get('profile_picture', None)
        )
        return user

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.address = validated_data.get('address', instance.address)
        
        
        if 'profile_picture' in validated_data:
            instance.profile_picture = validated_data.get('profile_picture')

        if 'password' in validated_data:
            instance.set_password(validated_data['password'])

        instance.save()
        return instance


class UserProfileSerializer(serializers.ModelSerializer):
    profile_picture_url = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['name', 'phone_number', 'email', 'address', 'profile_picture', 'profile_picture_url']
        read_only_fields = ['email']

    def get_profile_picture_url(self, obj):
        request = self.context.get('request')
        if obj.profile_picture and hasattr(obj.profile_picture, 'url'):
            return request.build_absolute_uri(obj.profile_picture.url)
        return None
