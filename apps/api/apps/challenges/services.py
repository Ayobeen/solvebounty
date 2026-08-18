from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError, PermissionDenied
from .models import Challenge
from apps.audit.models import AuditLog

class ChallengeService:
    @staticmethod
    def publish(challenge: Challenge, user) -> Challenge:
        if challenge.poster != user and not user.is_staff:
            raise PermissionDenied("Only the challenge poster can publish.")
        
        # Valid state check
        if challenge.status not in [Challenge.Status.DRAFT, Challenge.Status.PENDING_PAYMENT, Challenge.Status.FUNDED]:
            raise ValidationError(f"Cannot publish challenge with status: {challenge.status}")
        
        # If funded, transition to OPEN, else to PENDING_PAYMENT
        if challenge.status == Challenge.Status.FUNDED:
            challenge.status = Challenge.Status.OPEN
        else:
            # In MVP, if direct publishing is allowed without pre-payment, mark OPEN or PENDING_PAYMENT
            challenge.status = Challenge.Status.OPEN
            
        challenge.save()

        AuditLog.objects.create(
            actor=user,
            action=AuditLog.Action.CHALLENGE_PUBLISHED,
            entity='challenge',
            entity_id=challenge.id,
            metadata={'title': challenge.title, 'budget': str(challenge.budget)}
        )
        return challenge

    @staticmethod
    def cancel(challenge: Challenge, user, reason: str = "") -> Challenge:
        if challenge.poster != user and not user.is_staff:
            raise PermissionDenied("Only the poster or admin can cancel.")
        
        if challenge.status in [Challenge.Status.COMPLETED, Challenge.Status.CANCELLED]:
            raise ValidationError("Challenge is already completed or cancelled.")
        
        challenge.status = Challenge.Status.CANCELLED
        challenge.save()

        AuditLog.objects.create(
            actor=user,
            action='CHALLENGE_CANCELLED',
            entity='challenge',
            entity_id=challenge.id,
            metadata={'reason': reason}
        )
        return challenge

class WinnerSelectionService:
    @staticmethod
    @transaction.atomic
    def select(challenge: Challenge, user, submission_id: str, reason: str = "") -> dict:
        if challenge.poster != user and not user.is_staff:
            raise PermissionDenied("Only the challenge poster can select a winner.")
        
        if challenge.status not in [Challenge.Status.OPEN, Challenge.Status.CLOSED, Challenge.Status.JUDGING]:
            raise ValidationError(f"Cannot select winner when status is {challenge.status}")
        
        # Find submission
        from apps.submissions.models import Submission
        try:
            submission = Submission.objects.get(id=submission_id, challenge=challenge)
        except Submission.DoesNotExist:
            raise ValidationError("Submission does not belong to this challenge.")
        
        # Update submission status
        submission.status = Submission.Status.WINNER
        submission.save()

        # Update other submissions to REJECTED or FINALIST
        Submission.objects.filter(challenge=challenge).exclude(id=submission.id).update(
            status=Submission.Status.REJECTED
        )

        # Update challenge status and winner
        challenge.selected_winner = submission.solver
        challenge.status = Challenge.Status.WINNER_SELECTED
        challenge.save()

        # Update solver profile stats
        from decimal import Decimal
        from apps.profiles.models import Profile
        profile, _ = Profile.objects.get_or_create(user=submission.solver)
        profile.won_challenges += 1
        profile.completed_challenges += 1
        profile.reputation_score += Decimal('10.00')
        profile.save()

        # Audit log
        AuditLog.objects.create(
            actor=user,
            action=AuditLog.Action.WINNER_SELECTED,
            entity='challenge',
            entity_id=challenge.id,
            metadata={
                'submission_id': str(submission.id),
                'solver_id': str(submission.solver.id),
                'reason': reason,
                'amount': str(challenge.budget)
            }
        )

        return {
            "challenge_id": str(challenge.id),
            "status": challenge.status,
            "winner": {
                "submission_id": str(submission.id),
                "solver_id": str(submission.solver.id),
                "solver_name": submission.solver.full_name,
            },
            "payout": {
                "amount": float(challenge.budget),
                "currency": challenge.currency,
                "status": "PENDING"
            }
        }
