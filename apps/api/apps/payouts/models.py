import uuid
from django.db import models
from django.conf import settings
from apps.challenges.models import Challenge
from apps.submissions.models import Submission

class PayoutAccount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payout_account')
    provider = models.CharField(max_length=50, default='paystack')
    recipient_code = models.CharField(max_length=255, blank=True, default='')
    bank_code = models.CharField(max_length=20)
    bank_name = models.CharField(max_length=100, blank=True, default='')
    account_number = models.CharField(max_length=20)
    account_number_last4 = models.CharField(max_length=4, blank=True, default='')
    account_name = models.CharField(max_length=255)
    verified_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'payout_accounts'

    def save(self, *args, **kwargs):
        if self.account_number and not self.account_number_last4:
            self.account_number_last4 = self.account_number[-4:]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.account_name} - {self.bank_name} ({self.account_number_last4})"

class Payout(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        PROCESSING = 'PROCESSING', 'Processing'
        SUCCESS = 'SUCCESS', 'Success'
        FAILED = 'FAILED', 'Failed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='payouts')
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='payouts')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_payouts')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=3, default='NGN')
    provider_reference = models.CharField(max_length=255, unique=True, db_index=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING, db_index=True)
    failure_reason = models.TextField(blank=True, default='')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'payouts'
        ordering = ['-created_at']

    def __str__(self):
        return f"Payout {self.provider_reference} - {self.currency} {self.amount} ({self.status})"
