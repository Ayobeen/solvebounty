from rest_framework import viewsets, permissions, status, views
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .models import Challenge
from .serializers import ChallengeListSerializer, ChallengeDetailSerializer, ChallengeCreateSerializer
from .filters import ChallengeFilter
from .services import ChallengeService, WinnerSelectionService
from apps.accounts.permissions import IsPoster, IsOwnerOrReadOnly

class ChallengeViewSet(viewsets.ModelViewSet):
    queryset = Challenge.objects.select_related('poster', 'selected_winner').prefetch_related('skills', 'requirements', 'prize_allocations').all()
    filterset_class = ChallengeFilter
    search_fields = ['title', 'description', 'category', 'skills__name']
    ordering_fields = ['budget', 'deadline', 'created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return ChallengeCreateSerializer
        elif self.action in ['retrieve', 'update', 'partial_update']:
            return ChallengeDetailSerializer
        return ChallengeListSerializer

    def get_permissions(self):
        if self.action in ['create']:
            return [permissions.IsAuthenticated(), IsPoster()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsOwnerOrReadOnly()]
        return [permissions.AllowAny()]

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def publish(self, request, pk=None):
        challenge = self.get_object()
        updated_challenge = ChallengeService.publish(challenge, request.user)
        return Response(ChallengeDetailSerializer(updated_challenge).data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def cancel(self, request, pk=None):
        challenge = self.get_object()
        reason = request.data.get('reason', '')
        cancelled_challenge = ChallengeService.cancel(challenge, request.user, reason)
        return Response(ChallengeDetailSerializer(cancelled_challenge).data)

    @action(detail=True, methods=['post'], url_path='select-winner', permission_classes=[permissions.IsAuthenticated])
    def select_winner(self, request, pk=None):
        challenge = self.get_object()
        submission_id = request.data.get('submission_id')
        if not submission_id:
            return Response({'submission_id': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)
        reason = request.data.get('reason', '')
        result = WinnerSelectionService.select(
            challenge=challenge,
            user=request.user,
            submission_id=submission_id,
            reason=reason
        )
        return Response(result, status=status.HTTP_200_OK)
