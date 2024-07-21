import json
import requests

# api docs: https://todo.pixegami.io/docs
# api code: https://github.com/pixegami/todo-list-api
ENDPOINT = 'https://todo.pixegami.io'

def test_can_call_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200


def test_can_create_task():
    create_task_endpoint = f'{ENDPOINT}/create-task'
    payload = {
        "content": "test content",
        "user_id": "test_user_a3d",
        # "task_id": "task_id",
        "is_done": False
    }
    
    create_task_response = requests.put(create_task_endpoint, json=payload)
    assert create_task_response.status_code == 200
    
    create_task_data = create_task_response.json()
    print(create_task_data)
    task_id = create_task_data['task']['task_id']

    get_task_endpoint = f'{ENDPOINT}/get-task/{task_id}'
    get_task_response = requests.get(get_task_endpoint)
    assert get_task_response.status_code == 200

    get_task_data = get_task_response.json()
    print(get_task_data)
    print(get_task_data == create_task_data['task'])
    assert get_task_data == create_task_data['task']




