from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=254)

    USERNAME_FIELD = "email"



class Student(models.Model):
    user = models.OneToOneField(
        "students.User",
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="student",
    )

class Instructor(models.Model):
    user = models.OneToOneField(
        "students.User",
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="instructor",
    )