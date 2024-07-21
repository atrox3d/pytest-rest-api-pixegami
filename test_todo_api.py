import json
import requests
import uuid

# api docs: https://todo.pixegami.io/docs
# api code: https://github.com/pixegami/todo-list-api
ENDPOINT = 'https://todo.pixegami.io'

def get_payload():
    USER_ID = f'test_user_{uuid.uuid4().hex}'
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

def list_tasks(user_id):
    endpoint = f'{ENDPOINT}/list-tasks/{user_id}'
    response = requests.get(endpoint)
    return response

def delete_task(task_id):
    endpoint = f'{ENDPOINT}/delete-task/{task_id}'
    response = requests.delete(endpoint)
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

def test_can_list_tasks():
    total_tasks = 3
    payload = get_payload()
    user_id = payload['user_id']
    for _ in range(total_tasks):
        create_task_response = create_task(payload)
        assert create_task_response.status_code == 200
    
    list_task_response = list_tasks(user_id)
    assert list_task_response.status_code == 200
    
    data = list_task_response.json()
    print(data)
    tasks = data['tasks']
    assert len(tasks) == total_tasks

def test_can_delete_task():
    create_task_response = create_task(get_payload())
    assert create_task_response.status_code == 200
    
    create_task_data = create_task_response.json()
    task_id = create_task_data['task']['task_id']

    delete_task_response = delete_task(task_id)
    assert delete_task_response.status_code == 200

    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 404
