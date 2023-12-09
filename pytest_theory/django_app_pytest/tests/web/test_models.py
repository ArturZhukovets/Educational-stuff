import pytest
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_initial_user():
    count_users = User.objects.count()
    assert count_users == 1
