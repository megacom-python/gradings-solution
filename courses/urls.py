from django.urls import path
from courses import views


urlpatterns = [
    path("assignments/", views.AssignmentAPIView.as_view()),
    path(
        "assignments/<int:assignment_id>/submissions/",
        views.SubmissionAPIView.as_view(),
    ),
    path(
        "submissions/<int:pk>/",
        views.SubmissionUpdateAPIView.as_view()
    ),
    path("courses/", views.CourseAPIView.as_view()),
    path(
        "courses/<int:course_id>/add-student/<str:title>/",
        views.RegisterStudentToCourseAPIView.as_view(),
    ),
]
