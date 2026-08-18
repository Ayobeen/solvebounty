from django.db import IntegrityError
from rest_framework.exceptions import ValidationError, PermissionDenied
from .models import Submission
from apps.challenges.models import Challenge
from apps.audit.models import AuditLog

class SubmissionService:
    @staticmethod
    def create_submission(challenge_id: str, solver, data: dict) -> Submission:
        try:
            challenge = Challenge.objects.get(id=challenge_id)
        except Challenge.DoesNotExist:
            raise ValidationError({'challenge': 'Challenge not found.'})

        if challenge.status not in [Challenge.Status.OPEN, Challenge.Status.FUNDED]:
            raise ValidationError(f"Cannot submit to challenge in {challenge.status} status.")

        if challenge.poster == solver:
            raise ValidationError("You cannot submit a solution to your own challenge.")

        if Submission.objects.filter(challenge=challenge, solver=solver).exists():
            raise ValidationError("You have already submitted a solution to this challenge.")

        submission = Submission.objects.create(
            challenge=challenge,
            solver=solver,
            title=data.get('title', 'Solution Proposal'),
            content=data.get('content', ''),
            github_repo_url=data.get('github_repo_url', ''),
            live_demo_url=data.get('live_demo_url', '')
        )

        AuditLog.objects.create(
            actor=solver,
            action=AuditLog.Action.SUBMISSION_CREATED,
            entity='submission',
            entity_id=submission.id,
            metadata={'challenge_id': str(challenge.id), 'title': submission.title}
        )

        return submission

    @staticmethod
    def shortlist(submission: Submission, user) -> Submission:
        if submission.challenge.poster != user and not user.is_staff:
            raise PermissionDenied("Only the poster can shortlist submissions.")

        submission.status = Submission.Status.SHORTLISTED
        submission.save()

        AuditLog.objects.create(
            actor=user,
            action=AuditLog.Action.SUBMISSION_SHORTLISTED,
            entity='submission',
            entity_id=submission.id,
            metadata={'challenge_id': str(submission.challenge.id)}
        )
        return submission
