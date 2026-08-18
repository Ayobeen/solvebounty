import uuid
from django.db import models
from django.conf import settings

class AuditLog(models.Model):
    class Action(models.TextChoices):
        USER_REGISTERED = 'USER_REGISTERED', 'User Registered'
        CHALLENGE_CREATED = 'CHALLENGE_CREATED', 'Challenge Created'
        CHALLENGE_PUBLISHED = 'CHALLENGE_PUBLISHED', 'Challenge Published'
        CHALLENGE_FUNDED = 'CHALLENGE_FUNDED', 'Challenge Funded'
        PAYMENT_SUCCESS = 'PAYMENT_SUCCESS', 'Payment Success'
        SUBMISSION_CREATED = 'SUBMISSION_CREATED', 'Submission Created'
        SUBMISSION_SHORTLISTED = 'SUBMISSION_SHORTLISTED', 'Submission Shortlisted'
        WINNER_SELECTED = 'WINNER_SELECTED', 'Winner Selected'
        PAYOUT_CREATED = 'PAYOUT_CREATED', 'Payout Created'
        PAYOUT_SUCCESS = 'PAYOUT_SUCCESS', 'Payout Success'
        DISPUTE_OPENED = 'DISPUTE_OPENED', 'Dispute Opened'
        DISPUTE_RESOLVED = 'DISPUTE_RESOLVED', 'Dispute Resolved'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='audit_actions')
    action = models.CharField(max_length=50, choices=Action.choices, db_index=True)
    entity = models.CharField(max_length=50)  # challenge, submission, payment, payout, dispute
    entity_id = models.UUIDField(db_index=True)
    metadata = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'audit_logs'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.action} on {self.entity}:{self.entity_id} at {self.created_at}"
