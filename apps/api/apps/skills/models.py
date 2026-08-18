import uuid
from django.db import models
from django.conf import settings

class Skill(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True, db_index=True)
    category = models.CharField(max_length=100, blank=True, default='General')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'skills'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.category})"

class UserSkill(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='users')
    proficiency = models.SmallIntegerField(default=1)  # 1: Beginner, 2: Intermediate, 3: Expert, 4: Master

    class Meta:
        db_table = 'user_skills'
        unique_together = ('user', 'skill')

    def __str__(self):
        return f"{self.user.email} - {self.skill.name}"
