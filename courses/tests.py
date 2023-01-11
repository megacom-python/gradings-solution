import pytest
from django.urls import reverse
from rest_framework import status
from .factories import CourseFactory, SubmissionFactory
from students.factories import UserFactory
from students.models import Instructor, Student
from rest_framework.authtoken.models import Token
from unittest.mock import MagicMock
from courses.services.grades import GradeService

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
    submission = SubmissionFactory(grade=None)
    assert submission.grade is None
    url = reverse("grade_submission", kwargs={"pk": submission.id})
    response = api_client.put(url, data={
        "grade": faker.pyint(min_value=10, max_value=submission.assignment.points)
    }, format="json")
    assert response.status_code == status.HTTP_200_OK


def test_student_can_see_his_gpa(api_client, monkeypatch):
    fake_object = MagicMock()
    fake_object.return_value = {
        "avg": 200
    }
    monkeypatch.setattr(GradeService, "execute", fake_object)
    user = UserFactory()
    user.set_password("123!@#")
    user.save()
    student = Student.objects.create(user=user)
    submission = SubmissionFactory(student=student)
    token, _ = Token.objects.get_or_create(user=user)
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    url = reverse("gpa")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data.get("avg") != 200
