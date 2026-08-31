from django.contrib import admin
from .models import PayoutAccount, Payout

@admin.register(PayoutAccount)
class PayoutAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'account_name', 'bank_name', 'account_number_last4', 'verified_at')
    search_fields = ('user__email', 'account_name', 'account_number', 'bank_name')

@admin.register(Payout)
class PayoutAdmin(admin.ModelAdmin):
    list_display = ('provider_reference', 'recipient', 'challenge', 'amount', 'currency', 'status', 'created_at')
    list_filter = ('status', 'currency', 'created_at')
    search_fields = ('provider_reference', 'recipient__email', 'challenge__title')
    readonly_fields = ('id', 'created_at', 'updated_at')
