import uuid
from django.db import models
from django.utils.text import slugify
from django.conf import settings
from apps.skills.models import Skill

class Challenge(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        PENDING_PAYMENT = 'PENDING_PAYMENT', 'Pending Payment'
        FUNDED = 'FUNDED', 'Funded'
        OPEN = 'OPEN', 'Open'
        CLOSED = 'CLOSED', 'Closed'
        JUDGING = 'JUDGING', 'Judging'
        WINNER_SELECTED = 'WINNER_SELECTED', 'Winner Selected'
        DISPUTED = 'DISPUTED', 'Disputed'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    poster = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='challenges')
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    description = models.TextField()
    category = models.CharField(max_length=100, default='General')
    budget = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=3, default='NGN')
    platform_fee = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    deadline = models.DateTimeField()
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.DRAFT, db_index=True)
    visibility = models.CharField(max_length=20, default='PUBLIC')
    ip_terms = models.TextField(blank=True, default='')
    rules = models.TextField(blank=True, default='')
    skills = models.ManyToManyField(Skill, through='ChallengeSkill', related_name='challenges', blank=True)
    selected_winner = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='won_challenges'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'challenges'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or 'challenge'
            unique_part = str(uuid.uuid4())[:8]
            self.slug = f"{base_slug}-{unique_part}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.status}) - {self.currency} {self.budget}"

class ChallengeRequirement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='requirements')
    description = models.TextField()
    priority = models.SmallIntegerField(default=1)

    class Meta:
        db_table = 'challenge_requirements'
        ordering = ['priority', 'id']

class ChallengeSkill(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    class Meta:
        db_table = 'challenge_skills'
        unique_together = ('challenge', 'skill')

class PrizeAllocation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='prize_allocations')
    rank = models.SmallIntegerField()  # 1 for 1st place, 2 for 2nd place, etc.
    amount = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        db_table = 'prize_allocations'
        unique_together = ('challenge', 'rank')
        ordering = ['rank']
