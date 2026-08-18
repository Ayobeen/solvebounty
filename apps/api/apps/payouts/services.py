import uuid
from decimal import Decimal
from django.db import transaction
from rest_framework.exceptions import ValidationError, PermissionDenied
from .models import PayoutAccount, Payout
from apps.challenges.models import Challenge
from apps.submissions.models import Submission
from apps.payments.providers.paystack import PaystackProvider
from apps.ledger.services import LedgerService
from apps.audit.models import AuditLog

class PayoutService:
    @staticmethod
    def setup_payout_account(user, bank_code: str, bank_name: str, account_number: str, account_name: str) -> PayoutAccount:
        provider = PaystackProvider()
        recipient_data = provider.create_recipient(
            name=account_name,
            account_number=account_number,
            bank_code=bank_code
        )
        recipient_code = recipient_data.get('data', {}).get('recipient_code', '')

        account, _ = PayoutAccount.objects.update_or_create(
            user=user,
            defaults={
                'bank_code': bank_code,
                'bank_name': bank_name,
                'account_number': account_number,
                'account_name': account_name,
                'recipient_code': recipient_code,
            }
        )
        return account

    @staticmethod
    @transaction.atomic
    def release_payout(challenge_id: str, actor) -> Payout:
        try:
            challenge = Challenge.objects.select_for_update().get(id=challenge_id)
        except Challenge.DoesNotExist:
            raise ValidationError("Challenge not found.")

        if challenge.status != Challenge.Status.WINNER_SELECTED:
            raise ValidationError(f"Cannot payout challenge in {challenge.status} state. Winner must be selected.")

        if not challenge.selected_winner:
            raise ValidationError("No winner selected for this challenge.")

        winner = challenge.selected_winner
        try:
            payout_account = winner.payout_account
        except Exception:
            raise ValidationError("Winner has not configured a bank payout account yet.")

        # Find winning submission
        submission = Submission.objects.filter(challenge=challenge, solver=winner, status=Submission.Status.WINNER).first()
        if not submission:
            raise ValidationError("Winning submission record not found.")

        reference = f"PO_{uuid.uuid4().hex[:12].upper()}"
        amount = challenge.budget

        payout = Payout.objects.create(
            challenge=challenge,
            submission=submission,
            recipient=winner,
            amount=amount,
            currency=challenge.currency,
            provider_reference=reference,
            status=Payout.Status.PROCESSING
        )

        amount_kobo = int(amount * 100)
        provider = PaystackProvider()
        transfer_resp = provider.initiate_transfer(
            amount_kobo=amount_kobo,
            recipient_code=payout_account.recipient_code,
            reason=f"SolveBounty Prize: {challenge.title[:30]}",
            reference=reference
        )

        if not transfer_resp.get('status'):
            payout.status = Payout.Status.FAILED
            payout.failure_reason = transfer_resp.get('message', 'Transfer initiation failed')
            payout.save()
            raise ValidationError(f"Payout transfer error: {payout.failure_reason}")

        payout.status = Payout.Status.SUCCESS
        payout.save()

        # Atomic Ledger Debit
        LedgerService.record_payout(
            payout_id=payout.id,
            amount=amount,
            currency=challenge.currency
        )

        # Update Challenge to COMPLETED
        challenge.status = Challenge.Status.COMPLETED
        challenge.save()

        # Audit log
        AuditLog.objects.create(
            actor=actor,
            action=AuditLog.Action.PAYOUT_SUCCESS,
            entity='payout',
            entity_id=payout.id,
            metadata={'challenge_id': str(challenge.id), 'winner_id': str(winner.id), 'amount': str(amount)}
        )

        return payout
