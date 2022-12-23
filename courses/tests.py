import pytest
from django.urls import reverse
from rest_framework import status
from .factories import CourseFactory, SubmissionFactory
from students.factories import UserFactory
from students.models import Instructor
from rest_framework.authtoken.models import Token

pytestmark = pytest.mark.django_db

def test_list_courses(api_client):
    courses = CourseFactory.create_batch(size=10)
    url = reverse("courses_list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    for i, course in enumerate(courses):
        assert response.data[i].get("title") == course.title
        assert response.data[i].get("hours") == course.hours

def test_grade_submission(api_client, faker):
    user = UserFactory()
    user.set_password("123!@#")
    user.save()
    Instructor.objects.create(user=user)
    token, _ = Token.objects.get_or_create(user=user)
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    submission = SubmissionFactory()
    assert submission.grade is None
    url = reverse("grade_submission", kwargs={"pk": submission.id})
    response = api_client.put(url, data={
        "grade": faker.pyint(min_value=10, max_value=submission.assignment.points)
    }, format="json")
    assert response.status_code == status.HTTP_200_OK
