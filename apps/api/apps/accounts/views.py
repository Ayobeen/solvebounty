from rest_framework import status, views, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.utils import extend_schema
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from .services import AuthService

class RegisterView(views.APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(request=RegisterSerializer, responses={201: UserSerializer})
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        result = AuthService.register(
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            role=data.get('role', 'BOTH')
        )
        return Response({
            'user': UserSerializer(result['user']).data,
            'access_token': result['access_token'],
            'refresh_token': result['refresh_token'],
        }, status=status.HTTP_201_CREATED)

class LoginView(views.APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(request=LoginSerializer, responses={200: UserSerializer})
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = AuthService.login(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )
        return Response({
            'user': UserSerializer(result['user']).data,
            'access_token': result['access_token'],
            'refresh_token': result['refresh_token'],
        }, status=status.HTTP_200_OK)

class MeView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(responses={200: UserSerializer})
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @extend_schema(request=UserSerializer, responses={200: UserSerializer})
    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
