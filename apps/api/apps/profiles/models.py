import uuid
from django.db import models
from django.conf import settings

class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    username = models.CharField(max_length=100, unique=True, null=True, blank=True)
    bio = models.TextField(blank=True, default='')
    avatar_url = models.URLField(max_length=500, blank=True, default='')
    portfolio_url = models.URLField(max_length=500, blank=True, default='')
    github_url = models.URLField(max_length=500, blank=True, default='')
    reputation_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    completed_challenges = models.IntegerField(default=0)
    won_challenges = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'profiles'

    def __str__(self):
        return f"Profile of {self.user.email}"
