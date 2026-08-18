from rest_framework import serializers
from .models import Profile
from apps.accounts.serializers import UserSerializer

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = [
            'id', 'user', 'username', 'bio', 'avatar_url', 'portfolio_url',
            'github_url', 'reputation_score', 'completed_challenges', 'won_challenges',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'reputation_score', 'completed_challenges', 'won_challenges', 'created_at', 'updated_at']
