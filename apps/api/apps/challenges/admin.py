from django.contrib import admin
from .models import Challenge, ChallengeRequirement, ChallengeSkill, PrizeAllocation

class ChallengeRequirementInline(admin.TabularInline):
    model = ChallengeRequirement
    extra = 1

class ChallengeSkillInline(admin.TabularInline):
    model = ChallengeSkill
    extra = 1

class PrizeAllocationInline(admin.TabularInline):
    model = PrizeAllocation
    extra = 1

@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'poster', 'category', 'currency', 'budget', 'status', 'deadline', 'created_at')
    list_filter = ('status', 'category', 'currency', 'visibility', 'created_at')
    search_fields = ('title', 'description', 'poster__email', 'poster__first_name', 'poster__last_name', 'slug')
    readonly_fields = ('id', 'slug', 'created_at', 'updated_at')
    inlines = [ChallengeRequirementInline, ChallengeSkillInline, PrizeAllocationInline]
    actions = ['mark_as_cancelled', 'mark_as_open', 'mark_as_closed']

    @admin.action(description='Mark selected challenges as CANCELLED')
    def mark_as_cancelled(self, request, queryset):
        queryset.update(status=Challenge.Status.CANCELLED)

    @admin.action(description='Mark selected challenges as OPEN')
    def mark_as_open(self, request, queryset):
        queryset.update(status=Challenge.Status.OPEN)

    @admin.action(description='Mark selected challenges as CLOSED')
    def mark_as_closed(self, request, queryset):
        queryset.update(status=Challenge.Status.CLOSED)

@admin.register(ChallengeRequirement)
class ChallengeRequirementAdmin(admin.ModelAdmin):
    list_display = ('challenge', 'priority', 'description')
    search_fields = ('challenge__title', 'description')

@admin.register(PrizeAllocation)
class PrizeAllocationAdmin(admin.ModelAdmin):
    list_display = ('challenge', 'rank', 'amount')
    list_filter = ('rank',)
