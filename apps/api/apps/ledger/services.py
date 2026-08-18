from decimal import Decimal
from django.db import transaction
from .models import LedgerEntry

class LedgerService:
    @staticmethod
    @transaction.atomic
    def record_funding(payment_id, amount, currency='NGN', platform_fee=0):
        # Escrow Credit
        credit_entry = LedgerEntry.objects.create(
            reference_type='payment',
            reference_id=payment_id,
            entry_type=LedgerEntry.EntryType.CHALLENGE_FUNDING,
            amount=Decimal(str(amount)),
            currency=currency,
            direction=LedgerEntry.Direction.CREDIT,
            description=f"Received escrow funding for payment {payment_id}"
        )

        if platform_fee and Decimal(str(platform_fee)) > 0:
            LedgerEntry.objects.create(
                reference_type='payment',
                reference_id=payment_id,
                entry_type=LedgerEntry.EntryType.PLATFORM_FEE,
                amount=Decimal(str(platform_fee)),
                currency=currency,
                direction=LedgerEntry.Direction.CREDIT,
                description=f"Platform revenue fee for payment {payment_id}"
            )
        return credit_entry

    @staticmethod
    @transaction.atomic
    def record_payout(payout_id, amount, currency='NGN'):
        # Escrow Debit
        return LedgerEntry.objects.create(
            reference_type='payout',
            reference_id=payout_id,
            entry_type=LedgerEntry.EntryType.WINNER_PAYOUT,
            amount=Decimal(str(amount)),
            currency=currency,
            direction=LedgerEntry.Direction.DEBIT,
            description=f"Released bounty prize payout {payout_id}"
        )
