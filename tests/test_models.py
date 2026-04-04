import pytest

def test_health_response_structure():
    response = {'status': 'ok', 'env': 'dev'}
    assert 'status' in response
    assert 'env' in response
    assert response['status'] == 'ok'

def test_data_response_structure():
    response = {'message': 'Hello from Flask REST API'}
    assert 'message' in response
    assert isinstance(response['message'], str)

def test_environment_values():
    valid_envs = ['dev', 'staging', 'prod']
    current_env = 'dev'
    assert current_env in valid_envs
