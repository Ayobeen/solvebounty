import pytest
from apps.challenges.models import Challenge
from django.utils import timezone
from datetime import timedelta

@pytest.mark.django_db
def test_create_challenge(poster_auth_client):
    payload = {
        'title': 'Build Mobile App MVP',
        'description': 'Flutter or React Native app for logistics',
        'category': 'Mobile Development',
        'budget': 250000.00,
        'currency': 'NGN',
        'deadline': (timezone.now() + timedelta(days=20)).isoformat(),
        'requirements': ['Clean UI', 'API Integration', 'APK build'],
    }
    response = poster_auth_client.post('/api/v1/challenges/', payload, format='json')
    assert response.status_code == 201
    challenge_id = response.data['id']
    challenge = Challenge.objects.get(id=challenge_id)
    assert challenge.requirements.count() == 3
    assert challenge.status == Challenge.Status.DRAFT

@pytest.mark.django_db
def test_publish_challenge(poster_auth_client, sample_challenge):
    sample_challenge.status = Challenge.Status.DRAFT
    sample_challenge.save()

    response = poster_auth_client.post(f'/api/v1/challenges/{sample_challenge.id}/publish/')
    assert response.status_code == 200
    sample_challenge.refresh_from_db()
    assert sample_challenge.status == Challenge.Status.OPEN

@pytest.mark.django_db
def test_filter_challenges(api_client, sample_challenge):
    response = api_client.get('/api/v1/challenges/?category=Data+Analytics')
    assert response.status_code == 200
    assert len(response.data['results']) >= 1
