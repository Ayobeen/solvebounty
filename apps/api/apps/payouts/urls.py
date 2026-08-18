from django.urls import path
from .views import PayoutAccountView, InitiatePayoutView, MyPayoutsView

urlpatterns = [
    path('account/', PayoutAccountView.as_view(), name='payout-account'),
    path('release/<uuid:challenge_id>/', InitiatePayoutView.as_view(), name='payout-release'),
    path('me/', MyPayoutsView.as_view(), name='my-payouts'),
]
