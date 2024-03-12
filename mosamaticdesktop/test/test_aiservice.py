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
    return response.json()['tasks']


def task(token, name):
    response = requests.get(f'http://{HOST}:{PORT}/api/tasks/{name}', headers={
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
    (2)  Upload L3 images to task and retrieve fileset name
    (3)  Retrieve task definition you want and its parameters
    (4)  Set task parameters, including fileset name uploaded data
    (5)  Create task instance and submit parameters
    (6)  Retrieve task status
    (7)  If status = "finished", download output results
    """
    register('ralph', 'Arturo4ever', 'ralph.brecheisen@gmail.com', 'Ralph', 'Brecheisen')
    token = login('ralph', 'Arturo4ever')
    data = task(token=token, name='MuscleFatSegmentationTask')
    print(data)