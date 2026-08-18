from rest_framework import views, generics, permissions, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .models import Submission
from .serializers import SubmissionSerializer, SubmissionCreateSerializer
from .services import SubmissionService
from apps.accounts.permissions import IsSolver, IsOwnerOrReadOnly

class ChallengeSubmissionsView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(responses={200: SubmissionSerializer(many=True)})
    def get(self, request, challenge_id):
        # Solvers can only see their own submission; Poster or Admin can see all submissions
        submissions = Submission.objects.filter(challenge_id=challenge_id).select_related('solver', 'challenge')
        from apps.challenges.models import Challenge
        try:
            challenge = Challenge.objects.get(id=challenge_id)
            if challenge.poster != request.user and not request.user.is_staff:
                submissions = submissions.filter(solver=request.user)
        except Challenge.DoesNotExist:
            return Response({'detail': 'Challenge not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = SubmissionSerializer(submissions, many=True)
        return Response(serializer.data)

    @extend_schema(request=SubmissionCreateSerializer, responses={201: SubmissionSerializer})
    def post(self, request, challenge_id):
        serializer = SubmissionCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        submission = SubmissionService.create_submission(
            challenge_id=challenge_id,
            solver=request.user,
            data=serializer.validated_data
        )
        return Response(SubmissionSerializer(submission).data, status=status.HTTP_201_CREATED)

class SubmissionDetailView(generics.RetrieveAPIView):
    queryset = Submission.objects.select_related('solver', 'challenge').all()
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

class ShortlistSubmissionView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id):
        try:
            submission = Submission.objects.get(id=id)
        except Submission.DoesNotExist:
            return Response({'detail': 'Submission not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        updated = SubmissionService.shortlist(submission, request.user)
        return Response(SubmissionSerializer(updated).data)

class MySubmissionsView(generics.ListAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Submission.objects.filter(solver=self.request.user).select_related('challenge', 'solver')
