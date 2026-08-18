from rest_framework import serializers
from .models import Payment, PaymentEvent

class InitializePaymentSerializer(serializers.Serializer):
    challenge_id = serializers.UUIDField()
    callback_url = serializers.URLField(required=False, allow_blank=True)

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'challenge', 'payer', 'provider', 'provider_reference', 'amount', 'currency', 'status', 'metadata', 'created_at']
        read_only_fields = ['id', 'payer', 'provider', 'provider_reference', 'amount', 'currency', 'status', 'metadata', 'created_at']
