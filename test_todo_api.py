import json
import requests

# api docs: https://todo.pixegami.io/docs
# api code: https://github.com/pixegami/todo-list-api
ENDPOINT = 'https://todo.pixegami.io'

def test_can_call_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200


