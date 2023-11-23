import pytest
from flask import template_rendered
from contextlib import contextmanager
from src.controller import app

@pytest.fixture
def client():
    app.config.update({
        "TESTING": True,
    })
    with app.test_client() as client:
        yield client

@contextmanager
def captured_templates():
    recorded = []
    def record(sender, template, context, **extra):
        recorded.append((template, context))
    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)

def test_login_get(client):
    with captured_templates() as templates:
        response = client.get("/login")
        assert response.status_code == 200
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == '/templates/login.html'