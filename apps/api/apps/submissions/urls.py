from django.urls import path
from .views import ChallengeSubmissionsView, SubmissionDetailView, ShortlistSubmissionView, MySubmissionsView

urlpatterns = [
    path('challenges/<uuid:challenge_id>/submissions/', ChallengeSubmissionsView.as_view(), name='challenge-submissions'),
    path('submissions/<uuid:pk>/', SubmissionDetailView.as_view(), name='submission-detail'),
    path('submissions/<uuid:id>/shortlist/', ShortlistSubmissionView.as_view(), name='submission-shortlist'),
    path('me/submissions/', MySubmissionsView.as_view(), name='my-submissions'),
]
