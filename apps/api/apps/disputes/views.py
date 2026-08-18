from django.db import models
from rest_framework import serializers, viewsets, permissions, status
from rest_framework.response import Response
from .models import Dispute, DisputeEvidence
from apps.accounts.serializers import UserSerializer
from apps.challenges.models import Challenge
from apps.audit.models import AuditLog

class DisputeEvidenceSerializer(serializers.ModelSerializer):
    uploaded_by = UserSerializer(read_only=True)

    class Meta:
        model = DisputeEvidence
        fields = ['id', 'uploaded_by', 'title', 'description', 'file_url', 'created_at']

class DisputeSerializer(serializers.ModelSerializer):
    initiator = UserSerializer(read_only=True)
    evidence = DisputeEvidenceSerializer(many=True, read_only=True)

    class Meta:
        model = Dispute
        fields = ['id', 'challenge', 'submission', 'initiator', 'reason', 'desired_outcome', 'status', 'admin_resolution_notes', 'evidence', 'created_at', 'resolved_at']
        read_only_fields = ['id', 'initiator', 'status', 'admin_resolution_notes', 'resolved_at', 'created_at']

class DisputeViewSet(viewsets.ModelViewSet):
    queryset = Dispute.objects.select_related('challenge', 'submission', 'initiator').prefetch_related('evidence').all()
    serializer_class = DisputeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Dispute.objects.all()
        return Dispute.objects.filter(models.Q(initiator=user) | models.Q(challenge__poster=user) | models.Q(submission__solver=user)).distinct()

    def perform_create(self, serializer):
        challenge = serializer.validated_data['challenge']
        challenge.status = Challenge.Status.DISPUTED
        challenge.save()
        dispute = serializer.save(initiator=self.request.user)

        AuditLog.objects.create(
            actor=self.request.user,
            action=AuditLog.Action.DISPUTE_OPENED,
            entity='dispute',
            entity_id=dispute.id,
            metadata={'challenge_id': str(challenge.id), 'reason': dispute.reason}
        )
