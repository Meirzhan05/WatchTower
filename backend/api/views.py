from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.http import JsonResponse
from cliquepay.aws_cognito import CognitoService
from cliquepay.db_service import DatabaseService
from .serializers import *

@api_view(['GET'])
def api_root(request, format=None):
    """
    API root endpoint that provides links to all available endpoints
    """
    return Response({
        'endpoints': {
            'signup': {
                'url': reverse('register_user', request=request, format=format),
                'method': 'POST',
                'description': 'Register new user'
            },
            'verify': {
                'url': reverse('verify_signup', request=request, format=format),
                'method': 'POST',
                'description': 'Verify user email'
            },
            'resend-code': {
                'url': reverse('resend_code', request=request, format=format),
                'method': 'POST',
                'description': 'resend email verification code'
            },
            'login': {
                'url': reverse('user_login', request=request, format=format),
                'method': 'POST',
                'description': 'Log in user and get tokens',
                'tokens_provided': 'Refresh, Id, Access Tokens'
            },
            'refresh': {
                'url': reverse('renew_tokens', request=request, format=format),
                'method': 'POST',
                'description': 'Renew access and ID tokens using refresh token'
            },
            'logout': {
                'url': reverse('logout_user', request=request, format=format),
                'method': 'POST',
                'description': 'Logout the user by rendering the access and refresh tokens invalid'
            },
            'initiate-reset-password': {
                'url': reverse('initiate_reset_password', request=request, format=format),
                'method': 'POST',
                'description': 'Initiate password reset process'
            },
            'confirm-reset-password': {
                'url': reverse('confirm_reset_password', request=request, format=format),
                'method': 'POST',
                'description': 'Confirm password reset with verification code'
            },
            'friendlist': {
                'url': reverse('get_user_friends', request=request, format=format),
                'method': 'POST',
                'description': 'Extracts the user_sub from ID token,gets the user_id from database using user_sub and then makes a db query to get user friends using the user_id.'
            },
            'user-access': {
                'url': reverse('verify_user_access', request=request, format=format),
                'method': 'POST',
                'description': 'Posts the access token to aws and verfies if the user is registered.'
            },
            'user-profile': {
                'url': reverse('get_user_profile', request=request, format=format),
                'method': 'POST',
                'description': 'Gets the user details from the database.'
            }
        },
        'version': 'development',
        'status': 'online',
        'documentation': 'API documentation will be available soon ~yp'
    })

@api_view(['POST'])
def register_user(request):
    """
    Register a new user with AWS Cognito
    and store the user in database.
    
    Request body:
    {
        "username": "example_user",
        "fullname": "Jhon Doe",
        "password": "Example123!",
        "email": "user@example.com",
        "phone_number": "+1234567890" (optional)
    }
    """
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        cognito = CognitoService()
        result = cognito.register_user(**serializer.validated_data)
        
        if result['status'] == 'SUCCESS':
            return Response({
                'status': 'success',
                'message': result['message'],
                'user_sub': result.get('user_sub'),
                'next_step': 'Check your email for verification code'
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'status': 'error',
            'message': result['message'],
            'error_code': result.get('error_code'),
            'details': 'Registration failed'
        }, status=status.HTTP_400_BAD_REQUEST)
        
    return Response({
        'status': 'error',
        'message': 'Invalid input',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def verify_signup(request):
    """
    Verify user email with confirmation code
    
    Request body:
    {
        "username": "example_user",
        "confirmation_code": "123456"
    }
    """
    serializer = VerifySignupSerializer(data=request.data)
    if serializer.is_valid():
        cognito = CognitoService()
        result = cognito.confirm_sign_up(**serializer.validated_data)
        
        if result['status'] == 'SUCCESS':
            return Response({
                'status': 'success',
                'message': result['message'],
                'next_step': 'You can now login with your credentials'
            }, status=status.HTTP_200_OK)
        
        return Response({
            'status': 'error',
            'message': result['message'],
            'error_code': result.get('error_code'),
            'details': 'Verification failed'
        }, status=status.HTTP_400_BAD_REQUEST)
        
    return Response({
        'status': 'error',
        'message': 'Invalid input',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def user_login(request):
    """
    Login user with username and password
    
    Request body:
    {
        "username": "example_user",
        "password": "Example123!"
    }
    """
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        cognito = CognitoService()
        result = cognito.login_user(**serializer.validated_data)
        
        if result['status'] == 'SUCCESS':
            return Response({
                'status': 'success',
                'message': result['message'],
                'access_token': result['access_token'],
                'refresh_token': result['refresh_token'],
                'id_token': result['id_token']
            }, status=status.HTTP_200_OK)
        
        return Response({
            'status': 'error',
            'message': result['message'],
            'error_code': result.get('error_code'),
            'details': 'Verification failed'
        }, status=status.HTTP_400_BAD_REQUEST)
        
    return Response({
        'status': 'error',
        'message': 'Invalid input',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def renew_tokens(request):
    """
    Renew access and ID tokens using refresh token and id token
    
    Request body:
    {
        "refresh_token": "your-refresh-token",
        "id_token": "your-id-token"
    }
    """
    serializer = TokenRenewSerializer(data=request.data)
    if serializer.is_valid():
        cognito = CognitoService()
        result = cognito.renew_tokens(
            refresh_token=serializer.validated_data['refresh_token'],
            id_token=serializer.validated_data['id_token']
        )
        
        if result['status'] == 'SUCCESS':
            return Response(result, status=status.HTTP_200_OK)
        
        return Response(result, status=status.HTTP_401_UNAUTHORIZED)
        
    return Response({
        'status': 'error',
        'message': 'Invalid input',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout_user(request):
    """
    Pass the access token and make all the session tokens 
    including refresh token invalid, hence 'Logging Out' the user.
    
    Request body:
    {
        "access_token": "QwErTYuioP"
    }
    """
    serializer = LogoutUserSerializer(data=request.data)
    if serializer.is_valid():
        cognito = CognitoService()
        result = cognito.logout_user(serializer.validated_data['access_token'])
        
        if result['status'] == 'SUCCESS':
            return Response(result, status=status.HTTP_200_OK)
        
        return Response(result, status=status.HTTP_401_UNAUTHORIZED)
        
    return Response({
        'status': 'error',
        'message': 'Invalid input',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def initiate_reset_password(request):
    """
    Initiate password reset process
    
    Request body:
    {
        "id_token": "QwErTYuioP"
    }
    """
    serializer = InitiateResetPasswordSerializer(data=request.data)
    if serializer.is_valid():
        cognito = CognitoService()
        result = cognito.initiate_password_reset(serializer.validated_data['id_token'])
        
        if result['status'] == 'SUCCESS':
            return Response(result, status=status.HTTP_200_OK)
        
        return Response(result, status=status.HTTP_400_BAD_REQUEST)
        
    return Response({
        'status': 'error',
        'message': 'Invalid input',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def confirm_reset_password(request):
    """
    Confirm password reset with code
    
    Request body:
    {
        "id_token": "QwErTYuioP",
        "confirmation_code": "123456",
        "new_password": "NewPassword123!"
    }
    """
    serializer = ConfirmResetPasswordSerializer(data=request.data)
    if serializer.is_valid():
        cognito = CognitoService()
        result = cognito.confirm_password_reset(
            id_token=serializer.validated_data['id_token'],
            confirmation_code=serializer.validated_data['confirmation_code'],
            new_password=serializer.validated_data['new_password']
        )
        
        if result['status'] == 'SUCCESS':
            return Response(result, status=status.HTTP_200_OK)
        
        return Response(result, status=status.HTTP_400_BAD_REQUEST)
        
    return Response({
        'status': 'error',
        'message': 'Invalid input',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def get_user_friends(request):
    """
    Confirm password reset with code
    
    Request body:
    {
        "id_token": "QwErTYuioP",
    }
    """
    serializer = GetUserFriendsSerializer(data=request.data)
    if serializer.is_valid():
        cognito = CognitoService()
        firstResult = cognito.get_user_id(serializer.validated_data['id_token'])
        if firstResult['status'] == 'SUCCESS':
            db = DatabaseService()
            result = db.get_user_friends(firstResult.get('user_sub'))
            if result['status'] == 'SUCCESS':
                return Response(result, status=status.HTTP_200_OK)
        
        return Response({
            'status': 'error',
            'message': 'Could not verify user identity',
            'details': firstResult.get('message')
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    return Response({
        'status': 'error',
        'message': 'Invalid input',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def get_resend_code(request):
    """
    get the resent verification code through email.
    
    Request body:
    {
        "username": "example_user"
    }
    """
    serializer = GetResentVerificationCodeSerializer(data=request.data)
    if serializer.is_valid():
        cognito = CognitoService()
        result = cognito.resend_code(serializer.validated_data['username'])
        if result['status'] == 'SUCCESS':
            return Response(result, status=status.HTTP_200_OK)

        return Response(result, status=status.HTTP_400_BAD_REQUEST)

    return Response({
        'status': 'error',
        'message': 'Invalid input',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def verify_user_access(request):
    """
    confirm if the user is allowed to access certain or all pages.
    
    Request body:
    {
        "access_token" : "QwerTy"
    }
    """
    serializer = VerifyUserAccessSerializer(data=request.data)
    if serializer.is_valid():
        cognito = CognitoService()
        result = cognito.check_user_auth(serializer.validated_data['access_token'])
        if result['status'] == 'SUCCESS':
            return Response(result, status=status.HTTP_200_OK)
        return Response(result, status=status.HTTP_401_UNAUTHORIZED)
    
    return Response({
        'status': 'error',
        'message': 'Invalid input',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def get_user_profile(request):
    """
    Get the user profile from database by just providing the idToken.
    Returns user profile details.

    Request body:
    {
        "id_token" : "QwerTy"
    } 
    """
    serializer = GetUserProfileSerializer(data=request.data)
    if serializer.is_valid():
        cognito = CognitoService()
        getId = cognito.get_user_id(serializer.validated_data['id_token'])
        if getId['status'] == 'SUCCESS':
            db = DatabaseService()
            result = db.get_user_by_cognito_id(getId['user_sub'])
            if result['status'] == 'SUCCESS':
                return Response(result, status=status.HTTP_200_OK)
            return Response(result, status=status.HTTP_404_NOT_FOUND)
        return Response(getId, status=status.HTTP_401_UNAUTHORIZED)


    return Response({
        'status': 'error',
        'message': 'Invalid input',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)