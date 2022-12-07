from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=50)
    hours = models.PositiveSmallIntegerField(default=6)
    students = models.ManyToManyField("students.Student")


class Assignment(models.Model):
    course = models.ForeignKey("courses.Course", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    points = models.PositiveIntegerField(null=True)


class Submission(models.Model):
    assignment = models.ForeignKey(
        "courses.Assignment", on_delete=models.CASCADE
    )
    student = models.ForeignKey("students.Student", on_delete=models.CASCADE)
    content = models.TextField()
    grade = models.PositiveIntegerField(null=True)
