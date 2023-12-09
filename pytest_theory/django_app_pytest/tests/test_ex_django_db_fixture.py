import pytest
from django.contrib.auth.models import User

@pytest.fixture
def user(db):
    print("Creating fixture inside the fixture")
    return User.objects.create_user("Oleh")

@pytest.mark.django_db
def test_set_password(user):
    password = "Hello-world"
    user.set_password(password)
    assert user.check_password(password) is True


def test_username_without_db_access_using_only_fixture_value(user):
    assert user.username == "Oleh"


