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
    email = serializers.EmailField(required=True)
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
    email = serializers.EmailField(required=True)

class ConfirmResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
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

class VerifyUserAccessSerializer(serializers.Serializer):
    access_token = serializers.CharField(required=True)

class GetUserProfileSerializer(serializers.Serializer):
    id_token = serializers.CharField(required=True)

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        max_length=128, 
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        max_length=128, 
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    access_token = serializers.CharField(required=True)

class UpdateUserProfileSerializer(serializers.Serializer):
    id_token = serializers.CharField(required=True)
    full_name = serializers.CharField(required=False, max_length=150)
    phone_number = serializers.CharField(required=False, max_length=16)
    avatar_url = serializers.URLField(required=False)
    currency = serializers.CharField(required=False, max_length=10)

class FriendRequestSerializer(serializers.Serializer):
    id_token = serializers.CharField(required=True)
    recieve_username = serializers.CharField(max_length=255, required=False)
    recieve_useremail = serializers.EmailField(required=False)

    def validate(self, data):
        if not ('recieve_username' in data or 'recieve_useremail' in data):
            raise serializers.ValidationError("Either username or email must be provided")
        return data

class AcceptFriendRequestSerializer(serializers.Serializer):
    id_token = serializers.CharField(required=True)
    request_id = serializers.CharField(max_length=255, required=True)

class RemoveFriendSerializer(serializers.Serializer):
    id_token = serializers.CharField(required=True)
    friend_id = serializers.CharField(required=True)

class AddExpenseSerializer(serializers.Serializer):
    id_token = serializers.CharField(required=True)
    amount = serializers.FloatField(required=True)
    description = serializers.CharField(required=True)
    date = serializers.DateField(required=True)
    group_id = serializers.CharField(required=False)


