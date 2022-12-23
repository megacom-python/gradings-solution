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
        views.SubmissionUpdateAPIView.as_view(),
        name="grade_submission",
    ),
    path("courses/", views.CourseAPIView.as_view(), name="courses_list"),
    path(
        "courses/<int:course_id>/add-student/",
        views.RegisterStudentToCourseAPIView.as_view(),
    ),
    path(
        "gpa/", views.GradeInfoAPIView.as_view()
    ),
    path("courses/avg/<int:student_id>/", views.AvgPerCoursesAPIView.as_view())
]
