from app.tests.utils.utils import get_server_api, generate_access_token_headers, generate_random_username, \
    generate_random_email, generate_random_password
import requests
import json

access_token: str
username: str = generate_random_username()
email: str = generate_random_email()
password: str = generate_random_password()


# def test_register():
#     server_api = get_server_api()
#     payload = {'username': username, 'email': email, 'password': password}
#     response = requests.post(f'{server_api}/register', data=json.dumps(payload))
#     content = response.json()
#     assert response.status_code == 200
#     assert content['status'] == 'success'


def test_login_with_username():
    server_api = get_server_api()
    payload = {'username': username, 'password': password}
    response = requests.post(f'{server_api}/login', data=json.dumps(payload))
    content = response.json()
    assert response.status_code == 200
    assert content['status'] == 'success'
    assert 'token_type' in content['data']
    assert content['data']['token_type'] == 'bearer'
    assert 'access_token' in content['data']
    global access_token
    access_token = content['data']['access_token']


# def test_user_profile():
#     server_api = get_server_api()
#     global access_token
#     response = requests.get(f'{server_api}/profile', headers=generate_access_token_headers(access_token))
#     content = response.json()
#     assert response.status_code == 200
#     assert content['status'] == 'success'
#     assert 'uuid' in content['data']
#     assert 'username' in content['data']
#     assert 'email' in content['data']
#     assert 'mobile' in content['data']



