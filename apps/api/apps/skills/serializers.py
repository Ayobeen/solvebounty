from rest_framework import serializers
from .models import Skill, UserSkill

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'category', 'created_at']

class UserSkillSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(read_only=True)
    skill_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = UserSkill
        fields = ['skill', 'skill_id', 'proficiency']

    def create(self, validated_data):
        user = self.context['request'].user
        skill_id = validated_data.pop('skill_id')
        skill = Skill.objects.get(id=skill_id)
        user_skill, created = UserSkill.objects.update_or_create(
            user=user,
            skill=skill,
            defaults={'proficiency': validated_data.get('proficiency', 1)}
        )
        return user_skill
