import pytest
from unittest.mock import patch
from faker import Faker
from moto import mock_s3
from boto3.exceptions import S3UploadFailedError
from boto3.s3.transfer import S3Transfer
import boto3
from src.model.db.crud.s3_crud import s3_crud
import os
import uuid
from botocore.stub import Stubber
from botocore.exceptions import (BotoCoreError, ClientError, ParamValidationError,
                                 ReadTimeoutError, EndpointConnectionError)

@pytest.fixture(scope='function')
def aws_credentials():
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'

@pytest.fixture(scope='function')
def s3(aws_credentials):
    with mock_s3():
        s3 = boto3.client('s3', region_name='us-east-1')
        s3.create_bucket(Bucket='test-bucket')
        yield s3

@pytest.fixture(scope='function')
def test_directory(tmp_path):
    faker = Faker()
    directory = tmp_path / "test_files"
    directory.mkdir()
    for _ in range(5):
        file = directory / f"{faker.file_name(extension='html')}"
        file.write_text(faker.text())
    return directory

@pytest.fixture(scope='function')
def bucket_name():
    return 'test-bucket'

@pytest.fixture(scope='function')
def target_directory():
    return f'src/book/{str(uuid.uuid4())}'

@pytest.fixture
def css_test_directory(tmp_path):
    directory = tmp_path / "test_css"
    directory.mkdir()
    css_file = directory / "style.css"
    css_file.write_text("body { background-color: blue; }")
    return directory

def test_upload_to_s3_success(s3, test_directory, bucket_name, target_directory):
    s3_crud.upload_to_s3(bucket_name, str(test_directory), target_directory, s3)

def test_upload_to_nonexistent_bucket(s3, test_directory, target_directory):
    bucket_name = 'non-existent-bucket'
    with pytest.raises(S3UploadFailedError):
        s3_crud.upload_to_s3(bucket_name, str(test_directory), target_directory, s3)

def test_upload_raises_botocore_error(s3, test_directory, bucket_name, target_directory):
    with Stubber(s3) as stubber:
        stubber.add_client_error('upload_file', service_error_code='500')
        with pytest.raises(BotoCoreError):
            s3_crud.upload_to_s3(bucket_name, str(test_directory), target_directory, s3)

def test_upload_raises_generic_exception(s3, test_directory, bucket_name, target_directory):
    with patch.object(S3Transfer, 'upload_file', side_effect=Exception("Unexpected error")), \
            pytest.raises(Exception) as exc_info:
        s3_crud.upload_to_s3(bucket_name, str(test_directory), target_directory, s3)
    assert str(exc_info.value) == "Unexpected error"


def test_upload_css_file_content_type(s3, css_test_directory, bucket_name, target_directory):
    s3_crud.upload_to_s3(bucket_name, str(css_test_directory), target_directory, s3)
    response = s3.head_object(Bucket=bucket_name, Key=f'{target_directory}/style.css')
    assert 'ContentType' in response
    assert response['ContentType'] == 'text/css'