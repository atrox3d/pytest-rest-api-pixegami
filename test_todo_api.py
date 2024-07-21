import json
import requests

# api docs: https://todo.pixegami.io/docs
# api code: https://github.com/pixegami/todo-list-api
ENDPOINT = 'https://todo.pixegami.io'
USER_ID = 'test_user_a3d'

def get_payload():
    return {
        "content": "test content",
        "user_id": USER_ID,
        # "task_id": "task_id",
        "is_done": False
    }

def create_task(payload):
    endpoint = f'{ENDPOINT}/create-task'
    response = requests.put(endpoint, json=payload)
    return response

def update_task(payload):
    endpoint = f'{ENDPOINT}/update-task'
    response = requests.put(endpoint, json=payload)
    return response

def get_task(task_id):
    endpoint = f'{ENDPOINT}/get-task/{task_id}'
    response = requests.get(endpoint)
    return response

def test_can_call_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200

def test_can_create_task():
    create_task_response = create_task(get_payload())
    assert create_task_response.status_code == 200
    
    create_task_data = create_task_response.json()
    task_id = create_task_data['task']['task_id']

    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 200

    get_task_data = get_task_response.json()
    assert get_task_data == create_task_data['task']

def test_can_update_task():
    payload = get_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    
    create_task_data = create_task_response.json()
    task_id = create_task_data['task']['task_id']

    print(payload)
    payload.update({
        'task_id': task_id,
        'content': 'updated content',
        'is_done': True
    })
    update_task_response = update_task(payload)
    assert update_task_response.status_code == 200
    
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 200

    get_task_data = get_task_response.json()
    assert get_task_data['content'] == payload['content']
    assert get_task_data['is_done'] == payload['is_done']
