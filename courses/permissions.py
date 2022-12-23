from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from students.models import User


class IsStudentPermission(IsAuthenticated):
    def has_permission(self, request, view):
        is_authenticated = super().has_permission(request, view)
        # User.objects.filter(student=request.user.id).exists()
        # Student.objects.filter(user_id=request.user.id).exists()

        try:
            student = request.user.student
        except User.student.RelatedObjectDoesNotExist:
            return False
        return student and is_authenticated


class IsStudentOrReadOnly(IsStudentPermission):
    def has_permission(self, request, view):
        is_student = super().has_permission(request, view)
        return is_student or request.method in SAFE_METHODS


class IsInstructorPermission(IsAuthenticated):
    def has_permission(self, request, view):
        is_authenticated = super().has_permission(request, view)
        # User.objects.filter(student=request.user.id).exists()
        # Student.objects.filter(user_id=request.user.id).exists()
        try:
            instructor = request.user.instructor
        except (User.instructor.RelatedObjectDoesNotExist, AttributeError):
            return False
        return instructor and is_authenticated
