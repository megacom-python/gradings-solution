from rest_framework import generics
from .models import Assignment, Course, Submission
from .serializers import (
    AssignmentSerializer,
    CourseSerializer,
    SubmissionSerializer,
    ReadOnlySubmissionSerializer,
    UpdateSubmissionSerializer
)
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response
from rest_framework import status
from courses.permissions import IsStudentPermission, IsStudentOrReadOnly, IsInstructorPermission


class CourseAPIView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class AssignmentAPIView(generics.ListCreateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer


class RegisterStudentToCourseAPIView(generics.CreateAPIView):
    # serializer_class = RegisterStudentToCourseSerializer
    permission_classes = (IsStudentPermission,)

    def create(self, request, *args, **kwargs):
        course = Course.objects.get(id=kwargs.get("course_id"))
        course.students.add(request.user.student)
        return Response(
            {"details": f"You've been added to {course.title}"},
            status=status.HTTP_201_CREATED,
        )


class SubmissionAPIView(generics.ListCreateAPIView):
    lookup_url_kwarg = "assignment_id"
    # serializer_class = SubmissionSerializer
    permission_classes = (IsStudentOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method not in SAFE_METHODS:
            return SubmissionSerializer
        return ReadOnlySubmissionSerializer

    def get_queryset(self):
        queryset = Submission.objects.all()
        if self.request.method not in SAFE_METHODS:
            queryset = Assignment.objects.all()
        return queryset

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

class SubmissionUpdateAPIView(generics.UpdateAPIView):
    queryset = Submission.objects.all()
    serializer_class = UpdateSubmissionSerializer
    permission_classes = (IsInstructorPermission,)
