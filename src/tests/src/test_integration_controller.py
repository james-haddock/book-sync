from src.controller import app, get_s3_object_content, DatabaseManager, crud_book, CustomError
import pytest
from flask import render_template
import pytest
from moto import mock_s3
import boto3

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@pytest.mark.integration
def test_index_get(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == render_template('/templates/index.html')

@pytest.mark.integration
def test_login_get(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == render_template('/templates/login.html')

@pytest.mark.integration
def test_register_get(client):
    response = client.get('/register')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == render_template('/templates/register.html')

@pytest.mark.integration
def test_404_error(client):
    response = client.get('/nonexistentroute')
    assert response.status_code == 404

# def test_500_error(client):
#     response = client.get('/book/invaliduuid')
#     assert response.status_code == 500


@pytest.mark.integration
@mock_s3
def test_get_s3_object_content():
    s3 = boto3.client('s3', region_name='us-east-1')
    bucket_name = 'my-test-bucket'
    object_name = 'test_object.txt'
    s3.create_bucket(Bucket=bucket_name)
    s3.put_object(Bucket=bucket_name, Key=object_name, Body='Test content')

    content = get_s3_object_content(bucket_name, object_name, s3)
    assert content == 'Test content'

