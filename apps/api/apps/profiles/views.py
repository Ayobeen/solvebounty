from rest_framework import views, permissions, status, generics
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .models import Profile
from .serializers import ProfileSerializer

class MyProfileView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(responses={200: ProfileSerializer})
    def get(self, request):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    @extend_schema(request=ProfileSerializer, responses={200: ProfileSerializer})
    def patch(self, request):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class PublicProfileView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'user__id'
    lookup_url_kwarg = 'id'
