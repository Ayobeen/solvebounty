from rest_framework import serializers, generics, permissions
from .models import AuditLog
from apps.accounts.serializers import UserSerializer

class AuditLogSerializer(serializers.ModelSerializer):
    actor = UserSerializer(read_only=True)

    class Meta:
        model = AuditLog
        fields = ['id', 'actor', 'action', 'entity', 'entity_id', 'metadata', 'created_at']

class AuditLogListView(generics.ListAPIView):
    queryset = AuditLog.objects.select_related('actor').all()
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAdminUser]
    filterset_fields = ['action', 'entity']
