import pytest
import os
from src.models.models import db
from src.app import create_app


@pytest.fixture(scope="module")
def app():
    app = create_app()
    yield app


@pytest.fixture(scope="module")
def test_client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def clean_database(app):
    with app.app_context():
        db.session.remove()
        db.drop_all()
        db.create_all()
