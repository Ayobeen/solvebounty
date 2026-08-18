import pytest
from apps.accounts.models import User

@pytest.mark.django_db
def test_user_registration(api_client):
    payload = {
        'email': 'newuser@solvebounty.com',
        'password': 'StrongPassword123',
        'password_confirm': 'StrongPassword123',
        'first_name': 'Chidi',
        'last_name': 'Eze',
        'role': 'SOLVER'
    }
    response = api_client.post('/api/v1/auth/register/', payload)
    assert response.status_code == 201
    assert 'access_token' in response.data
    assert response.data['user']['email'] == 'newuser@solvebounty.com'
    
    # Verify profile created via signal
    user = User.objects.get(email='newuser@solvebounty.com')
    assert hasattr(user, 'profile')

@pytest.mark.django_db
def test_user_login(api_client, poster_user):
    payload = {
        'email': 'poster@solvebounty.com',
        'password': 'password123'
    }
    response = api_client.post('/api/v1/auth/login/', payload)
    assert response.status_code == 200
    assert 'access_token' in response.data
    assert response.data['user']['id'] == str(poster_user.id)

@pytest.mark.django_db
def test_authenticated_me_endpoint(poster_auth_client, poster_user):
    response = poster_auth_client.get('/api/v1/auth/me/')
    assert response.status_code == 200
    assert response.data['email'] == poster_user.email
