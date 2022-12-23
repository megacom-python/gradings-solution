from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
import pytest
from .models import User
from django.contrib.auth.hashers import check_password
from .factories import UserFactory
from rest_framework.authtoken.models import Token

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize("is_student", [True, False])
def test_register_user(api_client: APIClient, is_student: bool):
    data = {
        "email": "test@gmail.com",
        "password": "123!@#",
        "is_student": is_student
    }
    url = reverse("register_user")
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    user_id = response.json().get("id")
    user = User.objects.get(id=user_id)
    assert user.email == data.get("email")
    assert user.password != data.get("password")
    assert check_password(data.get("password"), user.password)
    assert hasattr(user, "instructor" if not is_student else "student")
    assert not hasattr(user, "instructor" if is_student else "student")


def test_register_user__invalid_body(api_client: APIClient):
    data = {
        "email": "test@gmail.com",
        "password": "123!@#",
    }
    url = reverse("register_user")
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'is_student': ['This field is required.']}


def test_register_user__invalid_email(api_client: APIClient):
    data = {
        "email": "testgmail.com",
        "password": "123!@#",
        "is_student": False
    }
    url = reverse("register_user")
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'email': ['Enter a valid email address.']}


def test_obtain_token_for_user(api_client: APIClient):
    user = UserFactory()
    user.set_password("123!@#")
    user.save()
    assert User.objects.count() > 0
    url = reverse("obtain_token")
    data = {
        "email": user.email,
        "password": "123!@#"
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    token = response.data.get("token")
    assert Token.objects.filter(key=token).exists()