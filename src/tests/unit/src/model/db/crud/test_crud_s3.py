import pytest
from faker import Faker
from moto import mock_s3
import boto3
from src.model.db.crud.s3_crud import s3_crud
import os
import uuid
from botocore.exceptions import BotoCoreError, ClientError
from botocore.stub import Stubber
from boto3.exceptions import S3UploadFailedError

@pytest.fixture(scope='function')
def aws_credentials():
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'

@pytest.fixture(scope='function')
def s3(aws_credentials):
    with mock_s3():
        yield boto3.client('s3', region_name='us-east-1')

@pytest.fixture(scope='function')
def test_directory(tmp_path):
    faker = Faker()
    directory = tmp_path / "test_files"
    directory.mkdir()
    for _ in range(5):
        file = directory / f"{faker.file_name(extension='txt')}"
        file.write_text(faker.text())
    return directory

def test_upload_to_s3_success(s3, test_directory):
    bucket_name = 'my-test-bucket'
    target_directory = f'src/book/{str(uuid.uuid4())}'
    s3.create_bucket(Bucket=bucket_name)
    s3_crud.upload_to_s3(bucket_name, str(test_directory), target_directory, s3)

def test_upload_to_s3_failure(s3, test_directory):

    bucket_name = 'non-existent-bucket'
    target_directory = f'src/book/{str(uuid.uuid4())}'
    with pytest.raises(Exception):
        s3_crud.upload_to_s3(bucket_name, str(test_directory), target_directory, s3)


def test_upload_to_invalid_bucket_failure(s3, test_directory):
    bucket_name = 'invalid-bucket'
    target_directory = f'src/book/{str(uuid.uuid4())}'
    with pytest.raises(Exception):
        s3_crud.upload_to_s3(bucket_name, str(test_directory), target_directory, s3)

def test_upload_raises_botocore_error(s3, test_directory):
    bucket_name = 'my-test-bucket'
    target_directory = f'src/book/{str(uuid.uuid4())}'
    s3.create_bucket(Bucket=bucket_name)

    with Stubber(s3) as stubber:
        stubber.add_client_error('upload_file', service_error_code='500')
        
        with pytest.raises(BotoCoreError):
            s3_crud.upload_to_s3(bucket_name, str(test_directory), target_directory, s3)


def test_upload_raises_client_error(s3, test_directory):
    bucket_name = 'my-test-bucket'
    target_directory = 'target'
    s3.create_bucket(Bucket=bucket_name)

    with Stubber(s3) as stubber:
        stubber.add_client_error('put_object', service_error_code='NoSuchBucket')
        
        with pytest.raises(S3UploadFailedError):
            s3_crud.upload_to_s3(bucket_name, str(test_directory), target_directory, s3)


@pytest.fixture
def css_test_directory(tmp_path):
    directory = tmp_path / "test_css"
    directory.mkdir()
    css_file = directory / "style.css"
    css_file.write_text("body { background-color: blue; }")
    return directory

def test_upload_css_file_content_type(s3, css_test_directory):
    bucket_name = 'my-test-bucket'
    target_directory = f'src/book/{str(uuid.uuid4())}'
    s3.create_bucket(Bucket=bucket_name)
    s3_crud.upload_to_s3(bucket_name, str(css_test_directory), target_directory, s3)
    response = s3.head_object(Bucket=bucket_name, Key=f'{target_directory}/style.css')
    assert 'ContentType' in response
    assert response['ContentType'] == 'text/css'