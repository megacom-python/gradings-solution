import factory

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "students.User"

    email = factory.Faker("email")
    # password = "123!@#"

class StudentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "students.Student"

    user = factory.SubFactory(UserFactory)


