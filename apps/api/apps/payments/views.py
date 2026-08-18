import json
from rest_framework import views, permissions, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .serializers import InitializePaymentSerializer, PaymentSerializer
from .services import PaymentService
from .models import Payment

class InitializePaymentView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(request=InitializePaymentSerializer)
    def post(self, request):
        serializer = InitializePaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = PaymentService.initialize_funding(
            challenge_id=serializer.validated_data['challenge_id'],
            payer=request.user,
            callback_url=serializer.validated_data.get('callback_url')
        )
        return Response(result, status=status.HTTP_200_OK)

class VerifyPaymentView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, reference):
        payment = PaymentService.verify_and_fulfill(reference)
        return Response(PaymentSerializer(payment).data)

class PaystackWebhookView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        signature = request.headers.get('x-paystack-signature', '')
        try:
            payload = json.loads(request.body.decode('utf-8'))
        except Exception:
            return Response({'error': 'Invalid JSON body'}, status=status.HTTP_400_BAD_REQUEST)

        result = PaymentService.handle_webhook(
            payload=payload,
            signature=signature,
            raw_body=request.body
        )
        return Response(result, status=status.HTTP_200_OK)

class MyPaymentsView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        payments = Payment.objects.filter(payer=request.user)
        return Response(PaymentSerializer(payments, many=True).data)
