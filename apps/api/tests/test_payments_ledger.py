import pytest
from apps.payments.models import Payment
from apps.challenges.models import Challenge
from apps.ledger.models import LedgerEntry
from apps.payments.services import PaymentService

@pytest.mark.django_db
def test_initialize_payment(poster_auth_client, sample_challenge):
    sample_challenge.status = Challenge.Status.DRAFT
    sample_challenge.save()

    response = poster_auth_client.post('/api/v1/payments/initialize/', {'challenge_id': str(sample_challenge.id)})
    assert response.status_code == 200
    assert 'reference' in response.data
    assert response.data['amount'] == float(sample_challenge.budget + sample_challenge.platform_fee)

@pytest.mark.django_db
def test_payment_fulfillment_and_ledger(poster_user, sample_challenge):
    sample_challenge.status = Challenge.Status.PENDING_PAYMENT
    sample_challenge.save()

    init_res = PaymentService.initialize_funding(challenge_id=str(sample_challenge.id), payer=poster_user)
    reference = init_res['reference']

    # Fulfill payment
    payment = PaymentService.verify_and_fulfill(reference)
    assert payment.status == Payment.Status.SUCCESS

    # Verify Challenge transitioned to OPEN
    sample_challenge.refresh_from_db()
    assert sample_challenge.status == Challenge.Status.OPEN

    # Verify Ledger credit entries created
    entries = LedgerEntry.objects.filter(reference_id=payment.id)
    assert entries.filter(entry_type=LedgerEntry.EntryType.CHALLENGE_FUNDING).exists()
