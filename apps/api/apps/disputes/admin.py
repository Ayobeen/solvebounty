from django.contrib import admin
from .models import Dispute, DisputeEvidence

class DisputeEvidenceInline(admin.TabularInline):
    model = DisputeEvidence
    extra = 0

@admin.register(Dispute)
class DisputeAdmin(admin.ModelAdmin):
    list_display = ('challenge', 'initiator', 'status', 'resolved_by', 'created_at', 'resolved_at')
    list_filter = ('status', 'created_at')
    search_fields = ('challenge__title', 'initiator__email', 'reason')
    readonly_fields = ('id', 'created_at')
    inlines = [DisputeEvidenceInline]
