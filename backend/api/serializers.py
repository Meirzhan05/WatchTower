from rest_framework import serializers



class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255, required=True)
    fullname = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(
        max_length=128, 
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    email = serializers.EmailField(required=True)
    phone_number = serializers.CharField(max_length=20, required=False)


class VerifySignupSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255, required=True)
    confirmation_code = serializers.CharField(max_length=6, required=True)

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(
        max_length=128, 
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

class TokenRenewSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)
    id_token = serializers.CharField(required=True)

class LogoutUserSerializer(serializers.Serializer):
    access_token = serializers.CharField(required=True)

class InitiateResetPasswordSerializer(serializers.Serializer):
    id_token = serializers.CharField(required=True)

class ConfirmResetPasswordSerializer(serializers.Serializer):
    id_token = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(max_length=6, required=True)
    new_password = serializers.CharField(
        max_length=128, 
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    
class GetUserFriendsSerializer(serializers.Serializer):
    id_token = serializers.CharField(required=True)

class GetResentVerificationCodeSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255, required=True)