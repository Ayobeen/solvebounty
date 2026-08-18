from rest_framework import views, permissions, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .services import AIServiceClient

class AIDraftChallengeView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        raw_description = request.data.get('raw_description', '')
        if not raw_description or len(raw_description.strip()) < 10:
            return Response(
                {'error': 'Please provide a descriptive prompt (at least 10 characters).'},
                status=status.HTTP_400_BAD_REQUEST
            )
        result = AIServiceClient.draft_challenge(raw_description)
        return Response(result, status=status.HTTP_200_OK)

class AIEvaluateSubmissionView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        requirements = request.data.get('requirements', [])
        submission_content = request.data.get('submission_content', '')
        result = AIServiceClient.evaluate_submission(requirements, submission_content)
        return Response(result, status=status.HTTP_200_OK)
