from fastapi.testclient import TestClient

from app.main import ADMIN_TOKEN, app

client = TestClient(app)


def test_healthz() -> None:
    response = client.get('/healthz')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'


def test_signup_then_pending_then_approve_then_login() -> None:
    signup = client.post(
        '/auth/signup',
        json={
            'username': 'analyst1',
            'email': 'analyst1@example.com',
            'password': 'pass1234',
        },
    )
    assert signup.status_code == 200
    user_id = signup.json()['id']

    login_before_approval = client.post(
        '/auth/login',
        json={'email': 'analyst1@example.com', 'password': 'pass1234'},
    )
    assert login_before_approval.status_code == 403

    pending = client.get('/admin/users/pending', headers={'x-admin-token': ADMIN_TOKEN})
    assert pending.status_code == 200
    assert any(u['id'] == user_id for u in pending.json())

    approve = client.post(
        f'/admin/users/{user_id}/approve', headers={'x-admin-token': ADMIN_TOKEN}
    )
    assert approve.status_code == 200
    assert approve.json()['approved'] is True

    login_after_approval = client.post(
        '/auth/login',
        json={'email': 'analyst1@example.com', 'password': 'pass1234'},
    )
    assert login_after_approval.status_code == 200
    assert 'access_token' in login_after_approval.json()


def test_upload_csv_reject_non_csv() -> None:
    bad = client.post(
        '/datasets/upload',
        files={'file': ('test.txt', b'not,csv', 'text/plain')},
    )
    assert bad.status_code == 400

    good = client.post(
        '/datasets/upload',
        files={'file': ('sample.csv', b'id,amount\n1,2\n', 'text/csv')},
    )
    assert good.status_code == 200
    assert good.json()['rows_detected'] == 1
