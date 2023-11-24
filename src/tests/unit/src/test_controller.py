from src import controller
import pytest
from io import BytesIO
from flask import render_template
import pytest
from faker import Faker
from moto import mock_s3
import boto3
from src.model.db.crud.s3_crud import s3_crud
import os
from botocore.exceptions import BotoCoreError, ClientError
from botocore.stub import Stubber
from boto3.exceptions import S3UploadFailedError

@pytest.fixture
def client():
    with controller.app.test_client() as client:
        yield client

def test_index_get(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == render_template('/templates/index.html')
    
def test_login_get(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == render_template('/templates/login.html')
    
def test_register_get(client):
    response = client.get('/register')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == render_template('/templates/register.html')
    
def test_404_error(client):
    response = client.get('/nonexistentroute')
    assert response.status_code == 404

def test_500_error(client):
    response = client.get('/book/invaliduuid')
    assert response.status_code == 500