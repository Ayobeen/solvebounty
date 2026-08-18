from rest_framework import views, permissions, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .models import PayoutAccount, Payout
from .serializers import PayoutAccountSerializer, PayoutSerializer
from .services import PayoutService

class PayoutAccountView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            account = request.user.payout_account
            return Response(PayoutAccountSerializer(account).data)
        except PayoutAccount.DoesNotExist:
            return Response({'detail': 'No payout account configured.'}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(request=PayoutAccountSerializer)
    def post(self, request):
        data = request.data
        for f in ['bank_code', 'bank_name', 'account_number', 'account_name']:
            if not data.get(f):
                return Response({f: 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        account = PayoutService.setup_payout_account(
            user=request.user,
            bank_code=data['bank_code'],
            bank_name=data['bank_name'],
            account_number=data['account_number'],
            account_name=data['account_name']
        )
        return Response(PayoutAccountSerializer(account).data, status=status.HTTP_200_OK)

class InitiatePayoutView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, challenge_id):
        from apps.challenges.models import Challenge
        try:
            challenge = Challenge.objects.get(id=challenge_id)
            if challenge.poster != request.user and not request.user.is_staff:
                return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        except Challenge.DoesNotExist:
            return Response({'detail': 'Challenge not found.'}, status=status.HTTP_404_NOT_FOUND)

        payout = PayoutService.release_payout(challenge_id=challenge_id, actor=request.user)
        return Response(PayoutSerializer(payout).data, status=status.HTTP_200_OK)

class MyPayoutsView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        payouts = Payout.objects.filter(recipient=request.user)
        return Response(PayoutSerializer(payouts, many=True).data)
