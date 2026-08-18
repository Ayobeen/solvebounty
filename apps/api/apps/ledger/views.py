from rest_framework import serializers, generics, permissions
from .models import LedgerEntry

class LedgerEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = LedgerEntry
        fields = ['id', 'reference_type', 'reference_id', 'entry_type', 'amount', 'currency', 'direction', 'description', 'created_at']

class LedgerListView(generics.ListAPIView):
    queryset = LedgerEntry.objects.all()
    serializer_class = LedgerEntrySerializer
    permission_classes = [permissions.IsAdminUser]
