from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'username', 'reputation_score', 'completed_challenges', 'won_challenges', 'created_at')
    search_fields = ('user__email', 'username', 'bio')
    readonly_fields = ('id', 'created_at', 'updated_at')
