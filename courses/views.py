from rest_framework import generics
from .models import Assignment, Course, Submission
from .serializers import (
    AssignmentSerializer,
    CourseSerializer,
    SubmissionSerializer,
    ReadOnlySubmissionSerializer,
    UpdateSubmissionSerializer,
    GPASerializer
)
from django.db.models import Avg, F
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


class GradeInfoAPIView(generics.ListAPIView):
    permission_classes = (IsStudentPermission,)
    serializer_class = GPASerializer
    """
    HTTP GET /students/gpa/

    {
        "avg": 4.00
    }
    """

    def get(self, request, *args, **kwargs):
        # assignment.points = 10
        # submission.grade = 8

        # 10 - 100%
        # 8 - ?

        data = request.user.student.submissions.annotate(
            percent=F("grade") * 100 / F("assignment__points")
        ).aggregate(
            avg=Avg("percent")
        )
        serializer = self.get_serializer(data, many=False)
        return Response(serializer.data)
        # request.user.student.submissions.


class AvgPerCoursesAPIView(generics.ListAPIView):
    # serializer_class = GPASerializer

    def get(self, request, *args, **kwargs):
        student_id = kwargs.get("student_id")
        queryset = Course.objects.filter(
            students__user_id=student_id,
            assignment__submission__student_id=student_id
        )

        """
        course_id | percent
        -------------------
        1           18
        1           50
        1           63
        1           100
        1           2
        
        
        course_id  |  avg_grade
        ---------------------
        1             ?
        """
        data = queryset.annotate(
            percent=F("assignment__submission__grade") * 100 / F("assignment__points")
        ).aggregate(
            avg=Avg("percent")
        )
        """
        SELECT AVG(p.percent)
        FROM (
            SELECT submission.grade * 100 / assignment.points AS percent   
            FROM course        
            JOIN assignment ON course.id = assignment.course_id        
            JOIN submission ON assignment.id = submission.assignment_id
        ) AS p
        """

        """
        annotate -> QuerySet[Course]
        aggregate -> Mapping[str, Any]
        """
        serializer = GPASerializer(data, many=False)
        return Response(serializer.data)
