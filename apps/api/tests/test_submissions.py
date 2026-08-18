import pytest
from apps.submissions.models import Submission

@pytest.mark.django_db
def test_create_submission(solver_auth_client, sample_challenge, solver_user):
    payload = {
        'title': 'Production Ready PowerBI Dashboard',
        'content': 'Here is my complete solution with SQL queries and interactive drill-downs.',
        'github_repo_url': 'https://github.com/solver/sales-bi',
        'live_demo_url': 'https://app.powerbi.com/view/sample'
    }
    response = solver_auth_client.post(f'/api/v1/challenges/{sample_challenge.id}/submissions/', payload)
    assert response.status_code == 201
    assert response.data['title'] == payload['title']
    assert response.data['solver']['id'] == str(solver_user.id)

@pytest.mark.django_db
def test_duplicate_submission_blocked(solver_auth_client, sample_challenge):
    payload = {'title': 'Sol 1', 'content': 'First proposal'}
    res1 = solver_auth_client.post(f'/api/v1/challenges/{sample_challenge.id}/submissions/', payload)
    assert res1.status_code == 201

    # Second submission by same user to same challenge should be rejected
    res2 = solver_auth_client.post(f'/api/v1/challenges/{sample_challenge.id}/submissions/', payload)
    assert res2.status_code == 400
