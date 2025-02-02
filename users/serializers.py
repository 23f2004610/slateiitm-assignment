from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT authentication serializer that ensures the user logs in with the correct role.
    """
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        # Verify role matches
        input_role = self.initial_data.get('role')
        if input_role and input_role != user.role:
            raise serializers.ValidationError({"role": "Invalid role for this user."})

        data.update({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
        })
        return data

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'linked_student')
        read_only_fields = ('id',)

class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer for initiating a password reset request.
    """
    email = serializers.EmailField()

    def validate_email(self, value):
        """
        Validate if the email exists in the system.
        """
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError({"email": "No user found with this email address."})
        return value

class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for confirming a password reset.
    """
    password = serializers.CharField(write_only=True, style={'input_type': 'password'}, min_length=8)
    token = serializers.CharField()
    uidb64 = serializers.CharField()

    def validate(self, data):
        """
        Validate the reset token and update password if valid.
        """
        try:
            uid = force_str(urlsafe_base64_decode(data['uidb64']))
            user = User.objects.get(pk=uid)
            if not default_token_generator.check_token(user, data['token']):
                raise serializers.ValidationError({"token": "Invalid or expired reset token."})
            data['user'] = user
            return data
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError({"token": "Invalid reset token."})
