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
    response = requests.post(f'http://{HOST}:{PORT}/api/token', data={
        'username': username, 'password': password,
    })
    token = response.json()['access']
    return token


def tasks(token):
    response = requests.get(f'http://{HOST}:{PORT}/api/tasks/', headers={
        'Authorization': f'Bearer {token}',
    })
    return response.json()


def createTask(token, name, parameters):
    response = requests.post(f'http://{HOST}:{PORT}/api/tasks/create', data={
        'name': name, 'parameters': parameters,
    }, headers={
        'Authorization': f'Bearer {token}',
    })
    taskId = response.json()['task_id']
    return taskId


def uploadDataToTask(token, files, taskId):
    pass


##############################################################################################################
def test_AiService():
    """
    Steps to use the AI service:
    (1)  Register user and login
    (2)  Retrieve task list (names + required/optional parameters)
    (2)  Create task with given name and provide parameter values
    (3)  Upload L3 images to task
    (4)  Start task
    (5)  Retrieve task status
    (6)  If status = "finished", download output results
    """
    register('ralph', 'Arturo4ever', 'ralph.brecheisen@gmail.com', 'Ralph', 'Brecheisen')
    token = login('ralph', 'Arturo4ever')
    data = tasks(token=token)
    print(data)