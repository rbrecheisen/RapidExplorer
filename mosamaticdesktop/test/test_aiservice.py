import requests

HOST = 'localhost'
PORT = '8000'


def register(username, password, email, firstName, lastName):
    response = requests.post(f'http://{HOST}:{PORT}/api/users/register', data={
        'username': username, 'password': password, 'email': email, 'first_name': firstName, 'last_name': lastName,
    })
    data = response.json()
    return data


def login(username, password):
    response = requests.post(f'http://{HOST}:{PORT}/api/token/', data={
        'username': username, 'password': password,
    })
    token = response.json()['access']
    return token


def test_AiService():
    register('ralph', 'Arturo4ever', 'ralph.brecheisen@gmail.com', 'Ralph', 'Brecheisen')
    token = login('ralph', 'Arturo4ever')
    assert token