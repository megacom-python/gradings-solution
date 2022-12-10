from rest_framework import serializers
from typing import Dict, Any
from rest_framework.exceptions import ValidationError
from .models import Assignment, Course, Submission


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        exclude = ("students",)


class AssignmentSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(write_only=True)

    class Meta:
        model = Assignment
        exclude = ("course",)

    def create(self, validated_data: Dict[str, Any]):
        course_title = validated_data.pop("course_title")
        course, _ = Course.objects.get_or_create(title=course_title)
        return Assignment.objects.create(course=course, **validated_data)


class RegisterStudentToCourseSerializer(serializers.Serializer):
    course_id = serializers.IntegerField(write_only=True)

    def validate(self, attrs: Dict[str, Any]):
        course_id = attrs.pop("course_id")
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            raise ValidationError(
                detail={
                    "details": f"Course with id = `{course_id}` was not found."
                }
            )
        attrs["course"] = course
        return attrs

    def create(self, validated_data: Dict[str, Any]):
        course = validated_data.pop("course")
        student = self.context.get("request").user
        course.students.add(student)
        return course


class SubmissionSerializer(serializers.ModelSerializer):
    student = serializers.ReadOnlyField(source="student.id")
    assignment = serializers.ReadOnlyField(source="assignment_id")

    class Meta:
        model = Submission
        fields = "__all__"

class ReadOnlySubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = "__all__"
        depth = 1

class UpdateSubmissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Submission
        fields = ("grade",)

    def update(self, instance: Submission, validated_data):
        grade = validated_data.get("grade")
        if grade > instance.assignment.points:
            raise ValidationError(detail={
                "details": "Grade must not be greater than maximum points."
            })
        return super().update(instance, validated_data)