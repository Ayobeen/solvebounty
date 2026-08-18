from rest_framework import serializers
from .models import PayoutAccount, Payout
from apps.accounts.serializers import UserSerializer

class PayoutAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayoutAccount
        fields = ['id', 'bank_code', 'bank_name', 'account_number', 'account_number_last4', 'account_name', 'verified_at', 'created_at']
        read_only_fields = ['id', 'account_number_last4', 'verified_at', 'created_at']

class PayoutSerializer(serializers.ModelSerializer):
    recipient = UserSerializer(read_only=True)

    class Meta:
        model = Payout
        fields = ['id', 'challenge', 'submission', 'recipient', 'amount', 'currency', 'provider_reference', 'status', 'failure_reason', 'created_at']
        read_only_fields = ['id', 'recipient', 'provider_reference', 'status', 'failure_reason', 'created_at']
