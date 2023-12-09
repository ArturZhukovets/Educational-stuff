import pytest
from django.contrib.auth.models import User


@pytest.fixture(autouse=True)
def create_user(db):
    User.objects.create_user(username="Alex", password="Alexpassword")

