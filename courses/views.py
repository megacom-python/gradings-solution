from rest_framework import generics
from .models import Assignment, Course
from .serializers import (
    AssignmentSerializer,
    CourseSerializer,
    RegisterStudentToCourseSerializer,
    SubmissionSerializer,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import HttpRequest


class CourseAPIView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class AssignmentAPIView(generics.ListCreateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer


class RegisterStudentToCourseAPIView(generics.CreateAPIView):
    # serializer_class = RegisterStudentToCourseSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        course = Course.objects.get(id=kwargs.get("course_id"))
        course.students.add(request.user.student)
        return Response(
            {"details": f"You've been added to {course.title}"},
            status=status.HTTP_201_CREATED,
        )


class SubmissionAPIView(generics.CreateAPIView):
    queryset = Assignment.objects.all()
    lookup_url_kwarg = "assignment_id"
    serializer_class = SubmissionSerializer
    permission_classes = (IsAuthenticated,)

    # def create(self, request: HttpRequest, *args, **kwargs):
    #     self.check_permissions(request)
    #     # assignment: Assignment = self.get_object()
    #     student = request.user.student
    #     request.data.update(
    #         {"assignment": kwargs.get("assignment_id"), "student": student}
    #     )
    #     return super().create(request, *args, **kwargs)
    # serializer = self.get_serializer(data=request.data)
    # serializer.is_valid(raise_exception=True)
    # self.perform_create(serializer)
    # headers = self.get_success_headers(serializer.data)
    # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    def perform_create(self, serializer):
        serializer.save(
            assignment_id=self.kwargs.get("assignment_id"),
            student=self.request.user.student,
        )
