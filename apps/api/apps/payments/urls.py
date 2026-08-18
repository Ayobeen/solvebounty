from django.urls import path
from .views import InitializePaymentView, VerifyPaymentView, PaystackWebhookView, MyPaymentsView

urlpatterns = [
    path('initialize/', InitializePaymentView.as_view(), name='payment-initialize'),
    path('verify/<str:reference>/', VerifyPaymentView.as_view(), name='payment-verify'),
    path('webhook/', PaystackWebhookView.as_view(), name='payment-webhook'),
    path('me/', MyPaymentsView.as_view(), name='my-payments'),
]
