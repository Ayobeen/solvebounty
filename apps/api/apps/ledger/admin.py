from django.contrib import admin
from .models import LedgerEntry

@admin.register(LedgerEntry)
class LedgerEntryAdmin(admin.ModelAdmin):
    list_display = ('entry_type', 'direction', 'amount', 'currency', 'reference_type', 'reference_id', 'created_at')
    list_filter = ('entry_type', 'direction', 'currency', 'created_at')
    search_fields = ('reference_type', 'reference_id', 'description')
    readonly_fields = ('id', 'reference_type', 'reference_id', 'entry_type', 'amount', 'currency', 'direction', 'description', 'created_at')
