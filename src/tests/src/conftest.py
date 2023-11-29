import pytest
from faker import Faker
from moto import mock_s3
import boto3
from src.model.db.crud.s3_crud import s3_crud
import os
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

