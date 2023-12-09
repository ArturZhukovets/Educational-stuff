# import pytest
# from django.contrib.auth.models import User
#
#
# @pytest.mark.django_db
# def test_create_user():
#     print("Creating user...")
#     User.objects.create_user("Oleh")
#     assert User.objects.count() == 1
#
#
# @pytest.mark.django_db
# def test_no_user():
#     # После каждого теста база подчищается
#     assert User.objects.count() == 0
