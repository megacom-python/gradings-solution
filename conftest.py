import pytest
from rest_framework.test import APIClient
from students.models import User, Student
from rest_framework.authtoken.models import Token


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def api_student(api_client: APIClient):
    user = User(
        email="student@gmail.com",
    )
    user.set_password("123!@#")
    user.save()
    Student.objects.create(user=user)
    token, _ = Token.objects.get_or_create(user=user)
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    return api_client