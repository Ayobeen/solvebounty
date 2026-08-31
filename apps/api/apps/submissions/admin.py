from django.contrib import admin
from .models import Submission, SubmissionFile

class SubmissionFileInline(admin.TabularInline):
    model = SubmissionFile
    extra = 0

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('title', 'challenge', 'solver', 'status', 'ai_score', 'submitted_at')
    list_filter = ('status', 'submitted_at')
    search_fields = ('title', 'content', 'solver__email', 'challenge__title')
    readonly_fields = ('id', 'submitted_at', 'updated_at')
    inlines = [SubmissionFileInline]
    actions = ['mark_as_shortlisted', 'mark_as_finalist', 'mark_as_winner', 'mark_as_rejected']

    @admin.action(description='Mark selected as SHORTLISTED')
    def mark_as_shortlisted(self, request, queryset):
        queryset.update(status=Submission.Status.SHORTLISTED)

    @admin.action(description='Mark selected as FINALIST')
    def mark_as_finalist(self, request, queryset):
        queryset.update(status=Submission.Status.FINALIST)

    @admin.action(description='Mark selected as WINNER')
    def mark_as_winner(self, request, queryset):
        queryset.update(status=Submission.Status.WINNER)

    @admin.action(description='Mark selected as REJECTED')
    def mark_as_rejected(self, request, queryset):
        queryset.update(status=Submission.Status.REJECTED)
