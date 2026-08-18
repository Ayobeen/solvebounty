import uuid
from django.db import models
from django.conf import settings
from apps.challenges.models import Challenge
from apps.submissions.models import Submission

class Dispute(models.Model):
    class Status(models.TextChoices):
        OPEN = 'OPEN', 'Open'
        UNDER_REVIEW = 'UNDER_REVIEW', 'Under Review'
        RESOLVED_IN_FAVOR_OF_POSTER = 'RESOLVED_POSTER', 'Resolved in Favor of Poster'
        RESOLVED_IN_FAVOR_OF_SOLVER = 'RESOLVED_SOLVER', 'Resolved in Favor of Solver'
        CANCELLED = 'CANCELLED', 'Cancelled'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='disputes')
    submission = models.ForeignKey(Submission, null=True, blank=True, on_delete=models.SET_NULL, related_name='disputes')
    initiator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='initiated_disputes')
    reason = models.TextField()
    desired_outcome = models.TextField(blank=True, default='')
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.OPEN, db_index=True)
    admin_resolution_notes = models.TextField(blank=True, default='')
    resolved_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='resolved_disputes')
    
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'disputes'
        ordering = ['-created_at']

    def __str__(self):
        return f"Dispute on {self.challenge.title} by {self.initiator.email} ({self.status})"

class DisputeEvidence(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dispute = models.ForeignKey(Dispute, on_delete=models.CASCADE, related_name='evidence')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    file_url = models.URLField(max_length=500, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'dispute_evidence'
