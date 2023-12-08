import pytest
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import exc
from src.model.db.db_manager import DatabaseManager
import time

@pytest.fixture
def db_url_passwordless_for_assertion(postgresql):
    user = postgresql.info.user
    dbname = postgresql.info.dbname
    host = postgresql.info.host
    port = postgresql.info.port

    url = f'postgresql://{user}:***@{host}:{port}/{dbname}'
    return url

@pytest.mark.unit
def test_enter(postgresql, db_url, db_url_passwordless_for_assertion):
    with pytest.MonkeyPatch.context() as m:
        m.setenv("DATABASE_URL", db_url)
        manager = DatabaseManager()
        session = manager.__enter__()
        assert str(session.bind.url) == db_url_passwordless_for_assertion


@pytest.mark.unit  
def test_enter_exception(postgresql, db_url, db_url_passwordless_for_assertion):
    with pytest.MonkeyPatch.context() as m:
        m.setenv("DATABASE_URL", "wrong_url")
        manager = DatabaseManager()
        with pytest.raises(SQLAlchemyError):
            with manager:
                raise SQLAlchemyError("Simulated database error")

@pytest.mark.unit
def mock_rollback(*args, **kwargs):
    raise exc.SQLAlchemyError("Mocked rollback exception")

@pytest.mark.unit
def test_rollback_exception(monkeypatch):
    db_manager = DatabaseManager()
    session = db_manager.__enter__()
    monkeypatch.setattr(session, 'rollback', mock_rollback)

    with pytest.raises(exc.SQLAlchemyError) as excinfo:
        db_manager.__exit__(TypeError, "test error", None)

    assert "Mocked rollback exception" in str(excinfo.value)
