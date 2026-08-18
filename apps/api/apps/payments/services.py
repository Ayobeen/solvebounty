import uuid
from decimal import Decimal
from django.db import transaction
from rest_framework.exceptions import ValidationError, PermissionDenied
from .models import Payment, PaymentEvent
from .providers.paystack import PaystackProvider
from apps.challenges.models import Challenge
from apps.ledger.services import LedgerService
from apps.audit.models import AuditLog

class PaymentService:
    @staticmethod
    def initialize_funding(challenge_id: str, payer, callback_url: str = None) -> dict:
        try:
            challenge = Challenge.objects.get(id=challenge_id)
        except Challenge.DoesNotExist:
            raise ValidationError("Challenge not found.")

        if challenge.poster != payer and not payer.is_staff:
            raise PermissionDenied("Only the poster can fund this challenge.")

        if challenge.status in [Challenge.Status.FUNDED, Challenge.Status.OPEN, Challenge.Status.COMPLETED]:
            raise ValidationError(f"Challenge is already {challenge.status}.")

        total_amount = challenge.budget + challenge.platform_fee
        reference = f"SB_{uuid.uuid4().hex[:12].upper()}"

        payment = Payment.objects.create(
            challenge=challenge,
            payer=payer,
            provider='paystack',
            provider_reference=reference,
            amount=total_amount,
            currency=challenge.currency,
            status=Payment.Status.PENDING,
            metadata={
                'challenge_title': challenge.title,
                'budget': str(challenge.budget),
                'platform_fee': str(challenge.platform_fee)
            }
        )

        amount_kobo = int(total_amount * 100)
        provider = PaystackProvider()
        response = provider.initialize_payment(
            email=payer.email,
            amount_kobo=amount_kobo,
            reference=reference,
            callback_url=callback_url
        )

        if not response.get('status'):
            payment.status = Payment.Status.FAILED
            payment.save()
            raise ValidationError(f"Payment gateway error: {response.get('message')}")

        return {
            'payment_id': str(payment.id),
            'reference': reference,
            'amount': float(total_amount),
            'currency': challenge.currency,
            'authorization_url': response.get('data', {}).get('authorization_url', ''),
        }

    @staticmethod
    @transaction.atomic
    def verify_and_fulfill(reference: str) -> Payment:
        try:
            payment = Payment.objects.select_for_update().get(provider_reference=reference)
        except Payment.DoesNotExist:
            raise ValidationError("Payment reference not found.")

        # Idempotency check: if already successful, skip ledger duplicate
        if payment.status == Payment.Status.SUCCESS:
            return payment

        provider = PaystackProvider()
        verify_data = provider.verify_payment(reference)

        if not verify_data.get('status') or verify_data.get('data', {}).get('status') != 'success':
            payment.status = Payment.Status.FAILED
            payment.save()
            raise ValidationError("Transaction verification failed with gateway.")

        payment.status = Payment.Status.SUCCESS
        payment.save()

        # Atomic Ledger entries
        challenge = payment.challenge
        LedgerService.record_funding(
            payment_id=payment.id,
            amount=challenge.budget,
            currency=payment.currency,
            platform_fee=challenge.platform_fee
        )

        # Update challenge state machine to FUNDED -> OPEN
        challenge.status = Challenge.Status.OPEN
        challenge.save()

        # Audit log
        AuditLog.objects.create(
            actor=payment.payer,
            action=AuditLog.Action.PAYMENT_SUCCESS,
            entity='payment',
            entity_id=payment.id,
            metadata={'reference': reference, 'amount': str(payment.amount), 'challenge_id': str(challenge.id)}
        )

        AuditLog.objects.create(
            actor=payment.payer,
            action=AuditLog.Action.CHALLENGE_FUNDED,
            entity='challenge',
            entity_id=challenge.id,
            metadata={'budget': str(challenge.budget)}
        )

        return payment

    @staticmethod
    def handle_webhook(payload: dict, signature: str, raw_body: bytes) -> dict:
        provider = PaystackProvider()
        if not provider.verify_webhook_signature(raw_body, signature):
            raise PermissionDenied("Invalid webhook signature.")

        event_type = payload.get('event')
        data = payload.get('data', {})
        reference = data.get('reference')
        event_id = payload.get('id') or data.get('id')

        # Store immutable raw event
        payment = Payment.objects.filter(provider_reference=reference).first() if reference else None
        PaymentEvent.objects.create(
            payment=payment,
            event_type=event_type or 'unknown',
            provider_event_id=str(event_id) if event_id else None,
            payload=payload
        )

        if event_type == 'charge.success' and reference:
            PaymentService.verify_and_fulfill(reference)
            return {'status': 'processed', 'event': event_type, 'reference': reference}

        return {'status': 'ignored', 'event': event_type}
