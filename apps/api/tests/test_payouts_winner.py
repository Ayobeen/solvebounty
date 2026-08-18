import pytest
from apps.submissions.models import Submission
from apps.challenges.models import Challenge
from apps.challenges.services import WinnerSelectionService
from apps.payouts.services import PayoutService
from apps.payouts.models import Payout
from apps.ledger.models import LedgerEntry

@pytest.mark.django_db
def test_winner_selection_and_payout(poster_user, solver_user, sample_challenge):
    submission = Submission.objects.create(
        challenge=sample_challenge,
        solver=solver_user,
        title='Winning App',
        content='Full working solution'
    )

    # Configure winner's payout account
    PayoutService.setup_payout_account(
        user=solver_user,
        bank_code='058',
        bank_name='GTBank',
        account_number='0123456789',
        account_name='Tunde Adeleke'
    )

    # Poster selects winner
    res = WinnerSelectionService.select(
        challenge=sample_challenge,
        user=poster_user,
        submission_id=str(submission.id),
        reason='Best architecture and complete requirements'
    )
    assert res['status'] == Challenge.Status.WINNER_SELECTED

    # Release payout
    payout = PayoutService.release_payout(challenge_id=str(sample_challenge.id), actor=poster_user)
    assert payout.status == Payout.Status.SUCCESS

    # Verify challenge is now COMPLETED
    sample_challenge.refresh_from_db()
    assert sample_challenge.status == Challenge.Status.COMPLETED

    # Verify Ledger Debit entry
    assert LedgerEntry.objects.filter(reference_id=payout.id, entry_type=LedgerEntry.EntryType.WINNER_PAYOUT, direction=LedgerEntry.Direction.DEBIT).exists()
