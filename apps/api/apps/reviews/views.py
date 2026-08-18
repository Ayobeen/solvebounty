from rest_framework import serializers, viewsets, permissions, status
from rest_framework.response import Response
from .models import Review
from apps.accounts.serializers import UserSerializer
from apps.challenges.models import Challenge
from apps.profiles.models import Profile

class ReviewSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)
    recipient_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Review
        fields = ['id', 'challenge', 'author', 'recipient', 'recipient_id', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'author', 'recipient', 'created_at']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def create(self, validated_data):
        author = self.context['request'].user
        recipient_id = validated_data.pop('recipient_id')
        from apps.accounts.models import User
        recipient = User.objects.get(id=recipient_id)
        
        review = Review.objects.create(
            author=author,
            recipient=recipient,
            **validated_data
        )

        from decimal import Decimal
        profile, _ = Profile.objects.get_or_create(user=recipient)
        all_reviews = Review.objects.filter(recipient=recipient)
        avg = sum(r.rating for r in all_reviews) / all_reviews.count()
        profile.reputation_score = Decimal(str(round(avg, 2)))
        profile.save()

        return review

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related('author', 'recipient', 'challenge').all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_fields = ['challenge', 'recipient', 'rating']
