from django.urls import path
from .views import AIDraftChallengeView, AIEvaluateSubmissionView

urlpatterns = [
    path('draft/', AIDraftChallengeView.as_view(), name='ai-draft-challenge'),
    path('evaluate/', AIEvaluateSubmissionView.as_view(), name='ai-evaluate-submission'),
]
