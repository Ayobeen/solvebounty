import uuid
from django.db import models
from django.conf import settings
from apps.challenges.models import Challenge

class Submission(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        SUBMITTED = 'SUBMITTED', 'Submitted'
        SHORTLISTED = 'SHORTLISTED', 'Shortlisted'
        FINALIST = 'FINALIST', 'Finalist'
        WINNER = 'WINNER', 'Winner'
        REJECTED = 'REJECTED', 'Rejected'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='submissions')
    solver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='submissions')
    title = models.CharField(max_length=255, default='Solution')
    content = models.TextField()
    github_repo_url = models.URLField(max_length=500, blank=True, default='')
    live_demo_url = models.URLField(max_length=500, blank=True, default='')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SUBMITTED, db_index=True)
    ai_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    ai_feedback = models.TextField(blank=True, default='')
    
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'submissions'
        unique_together = ('challenge', 'solver')
        ordering = ['-submitted_at']

    def __str__(self):
        return f"Submission by {self.solver.email} on {self.challenge.title} ({self.status})"

class SubmissionFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='files')
    storage_key = models.CharField(max_length=500)
    filename = models.CharField(max_length=255)
    file_url = models.URLField(max_length=500, blank=True, default='')
    mime_type = models.CharField(max_length=150, blank=True, default='')
    file_size = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'submission_files'
