import uuid
from django.db import models

class LedgerEntry(models.Model):
    class EntryType(models.TextChoices):
        CHALLENGE_FUNDING = 'CHALLENGE_FUNDING', 'Challenge Funding'
        WINNER_PAYOUT = 'WINNER_PAYOUT', 'Winner Payout'
        PLATFORM_FEE = 'PLATFORM_FEE', 'Platform Fee'
        REFUND = 'REFUND', 'Refund'
        ADJUSTMENT = 'ADJUSTMENT', 'Adjustment'

    class Direction(models.TextChoices):
        CREDIT = 'CREDIT', 'Credit (Inflow to Platform Escrow)'
        DEBIT = 'DEBIT', 'Debit (Outflow to Recipient / Gateway)'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reference_type = models.CharField(max_length=50)  # e.g., 'payment', 'payout', 'challenge'
    reference_id = models.UUIDField(db_index=True)
    entry_type = models.CharField(max_length=50, choices=EntryType.choices)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=3, default='NGN')
    direction = models.CharField(max_length=10, choices=Direction.choices)
    description = models.TextField(blank=True, default='')
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ledger_entries'
        ordering = ['-created_at']

    def __str__(self):
        return f"Ledger {self.direction} {self.amount} {self.currency} for {self.reference_type}:{self.reference_id}"
