from django.contrib import admin
from .models import Payment, PaymentEvent

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('provider_reference', 'challenge', 'payer', 'amount', 'currency', 'status', 'created_at')
    list_filter = ('status', 'currency', 'provider', 'created_at')
    search_fields = ('provider_reference', 'payer__email', 'challenge__title')
    readonly_fields = ('id', 'created_at', 'updated_at')

@admin.register(PaymentEvent)
class PaymentEventAdmin(admin.ModelAdmin):
    list_display = ('event_type', 'payment', 'provider_event_id', 'received_at')
    list_filter = ('event_type', 'received_at')
    readonly_fields = ('id', 'received_at')
