from rest_framework import serializers
from .models import Submission, SubmissionFile
from apps.accounts.serializers import UserSerializer

class SubmissionFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionFile
        fields = ['id', 'storage_key', 'filename', 'file_url', 'mime_type', 'file_size', 'created_at']

class SubmissionSerializer(serializers.ModelSerializer):
    solver = UserSerializer(read_only=True)
    files = SubmissionFileSerializer(many=True, read_only=True)

    class Meta:
        model = Submission
        fields = [
            'id', 'challenge', 'solver', 'title', 'content', 'github_repo_url',
            'live_demo_url', 'status', 'ai_score', 'ai_feedback', 'files',
            'submitted_at', 'updated_at'
        ]
        read_only_fields = ['id', 'solver', 'status', 'ai_score', 'ai_feedback', 'submitted_at', 'updated_at']

class SubmissionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['title', 'content', 'github_repo_url', 'live_demo_url']
