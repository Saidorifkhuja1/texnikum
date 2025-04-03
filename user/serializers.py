from rest_framework import serializers
from .models import  User
from django.core.mail import send_mail
from django.conf import settings
from .utils import generate_verification_link
from django.core.mail import EmailMessage

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate

class SendVerificationCodeSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=250)
    last_name = serializers.CharField(max_length=250)
    # phone_number = serializers.CharField(max_length=20)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=4, write_only=True)


class VerifyCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(min_length=6, max_length=6)




class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['uid', 'phone_number', 'name', 'last_name', 'email', 'avatar']


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'last_name', 'email', 'avatar']
        read_only_fields = ['phone_number']

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)

        if 'avatar' in validated_data:
            instance.avatar = validated_data['avatar']

        instance.save()
        return instance





class PasswordResetSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    class Meta:
        fields = ['old_password', 'new_password']

    def validate(self, data):
        if data['old_password'] == data['new_password']:
            raise serializers.ValidationError("The new password cannot be the same as the old password.")
        return data









class PasswordResetRequestSerializer(serializers.Serializer):

    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):

    email = serializers.EmailField()
    code = serializers.CharField(min_length=6, max_length=6)
    new_password = serializers.CharField(min_length=6)








class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        # Check if email exists in DB
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"detail": "Email not registered"})

        # Authenticate user
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError({"detail": "Incorrect email or password"})

        # Check if user is active
        if not user.is_active:
            raise serializers.ValidationError({"detail": "This account is inactive"})

        return super().validate(attrs)

