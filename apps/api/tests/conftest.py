import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from apps.accounts.models import User
from apps.challenges.models import Challenge
from apps.skills.models import Skill
from django.utils import timezone
from datetime import timedelta

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def poster_user(db):
    return User.objects.create_user(
        email='poster@solvebounty.com',
        password='password123',
        first_name='Amaka',
        last_name='Okeke',
        role=User.Role.POSTER
    )

@pytest.fixture
def solver_user(db):
    return User.objects.create_user(
        email='solver@solvebounty.com',
        password='password123',
        first_name='Tunde',
        last_name='Adeleke',
        role=User.Role.SOLVER
    )

@pytest.fixture
def poster_auth_client(api_client, poster_user):
    token = str(RefreshToken.for_user(poster_user).access_token)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return api_client

@pytest.fixture
def solver_auth_client(api_client, solver_user):
    token = str(RefreshToken.for_user(solver_user).access_token)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return api_client

@pytest.fixture
def sample_challenge(db, poster_user):
    return Challenge.objects.create(
        poster=poster_user,
        title='Build Sales Dashboard',
        description='Need high performance dashboard in Power BI or React',
        category='Data Analytics',
        budget=100000.00,
        currency='NGN',
        platform_fee=10000.00,
        deadline=timezone.now() + timedelta(days=14),
        status=Challenge.Status.OPEN
    )
