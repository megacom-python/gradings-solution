import factory
from students.factories import StudentFactory


class CourseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "courses.Course"

    title = factory.Faker("word")
    hours = factory.Faker("pyint", min_value=2, max_value=6, step=2)


class AssignmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "courses.Assignment"

    course = factory.SubFactory(CourseFactory)
    title = factory.Faker("word")
    description = factory.Faker("paragraph")
    points = factory.Faker("pyint", min_value=10, max_value=100)


class SubmissionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "courses.Submission"

    assignment = factory.SubFactory(AssignmentFactory)
    content = factory.Faker("paragraph")
    student = factory.SubFactory(StudentFactory)
    grade = factory.Faker("pyint", min_value=10, max_value=100)