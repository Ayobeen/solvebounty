from rest_framework import serializers
from .models import Challenge, ChallengeRequirement, PrizeAllocation
from apps.skills.models import Skill
from apps.skills.serializers import SkillSerializer
from apps.accounts.serializers import UserSerializer

class RequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChallengeRequirement
        fields = ['id', 'description', 'priority']

class PrizeAllocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrizeAllocation
        fields = ['id', 'rank', 'amount']

class ChallengeListSerializer(serializers.ModelSerializer):
    poster = UserSerializer(read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    submission_count = serializers.IntegerField(source='submissions.count', read_only=True)

    class Meta:
        model = Challenge
        fields = [
            'id', 'poster', 'title', 'slug', 'description', 'category',
            'budget', 'currency', 'platform_fee', 'deadline', 'status',
            'visibility', 'skills', 'submission_count', 'created_at', 'updated_at'
        ]

class ChallengeDetailSerializer(serializers.ModelSerializer):
    poster = UserSerializer(read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    requirements = RequirementSerializer(many=True, read_only=True)
    prize_allocations = PrizeAllocationSerializer(many=True, read_only=True)
    selected_winner = UserSerializer(read_only=True)
    submission_count = serializers.IntegerField(source='submissions.count', read_only=True)

    class Meta:
        model = Challenge
        fields = [
            'id', 'poster', 'title', 'slug', 'description', 'category',
            'budget', 'currency', 'platform_fee', 'deadline', 'status',
            'visibility', 'ip_terms', 'rules', 'skills', 'requirements',
            'prize_allocations', 'selected_winner', 'submission_count',
            'created_at', 'updated_at'
        ]

class ChallengeCreateSerializer(serializers.ModelSerializer):
    requirements = serializers.ListField(
        child=serializers.CharField(max_length=500), write_only=True, required=False
    )
    skill_ids = serializers.ListField(
        child=serializers.UUIDField(), write_only=True, required=False
    )
    prizes = serializers.ListField(
        child=serializers.DictField(), write_only=True, required=False
    )

    class Meta:
        model = Challenge
        fields = [
            'id', 'title', 'description', 'category', 'budget', 'currency',
            'deadline', 'ip_terms', 'rules', 'requirements', 'skill_ids', 'prizes'
        ]

    def create(self, validated_data):
        requirements_data = validated_data.pop('requirements', [])
        skill_ids = validated_data.pop('skill_ids', [])
        prizes_data = validated_data.pop('prizes', [])
        
        user = self.context['request'].user
        from decimal import Decimal
        budget_val = Decimal(str(validated_data.get('budget', 0)))
        challenge = Challenge.objects.create(
            poster=user,
            platform_fee=budget_val * Decimal('0.10'),  # 10% platform fee
            **validated_data
        )

        for idx, req_text in enumerate(requirements_data):
            ChallengeRequirement.objects.create(
                challenge=challenge,
                description=req_text,
                priority=idx + 1
            )

        if skill_ids:
            skills = Skill.objects.filter(id__in=skill_ids)
            challenge.skills.set(skills)

        if prizes_data:
            for prize in prizes_data:
                PrizeAllocation.objects.create(
                    challenge=challenge,
                    rank=prize.get('rank', 1),
                    amount=prize.get('amount', challenge.budget)
                )
        else:
            # Default 100% to 1st place
            PrizeAllocation.objects.create(
                challenge=challenge,
                rank=1,
                amount=challenge.budget
            )

        return challenge
