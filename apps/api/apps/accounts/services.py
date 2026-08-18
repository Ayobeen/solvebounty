from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User

class AuthService:
    @staticmethod
    def register(email, password, first_name, last_name, role='BOTH'):
        if User.objects.filter(email=email).exists():
            raise ValidationError({'email': 'A user with this email already exists.'})
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role=role
        )
        refresh = RefreshToken.for_user(user)
        return {
            'user': user,
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        }

    @staticmethod
    def login(email, password):
        user = authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed('Invalid email or password.')
        if user.status != User.Status.ACTIVE:
            raise AuthenticationFailed('Account is suspended or inactive.')
        refresh = RefreshToken.for_user(user)
        return {
            'user': user,
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        }
