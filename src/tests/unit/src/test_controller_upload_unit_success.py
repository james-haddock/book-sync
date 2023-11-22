import tempfile
from flask import url_for, flash
from unittest.mock import MagicMock
from src.controller import s3, aws_bucket
import uuid
from faker import Faker

fake = Faker()

