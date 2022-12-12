from rest_framework import serializers
from students.models import User, Student, Instructor
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token


class RegisterUserSerializer(serializers.ModelSerializer):
    is_student = serializers.BooleanField(write_only=True)

    class Meta:
        model = User
        fields = "__all__"

    def validate(self, attrs):
        attrs["password"] = make_password(attrs["password"])
        return attrs

    def create(self, validated_data):
        is_student = validated_data.pop("is_student")
        user = super().create(validated_data)
        role_cls = Student if is_student else Instructor
        role_cls.objects.create(user=user)
        return user


class ObtainTokenSerializer(serializers.Serializer):
    token = serializers.CharField(read_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        fields = "__all__"
        # extra_kwargs = {
        #     "password": {"write_only": True},
        #     "email": {"write_only": True},
        # }

    def create(self, validated_data):
        instance = User.objects.get(email=validated_data.get("email"))
        if not check_password(
                validated_data.get("password"), instance.password
        ):
            raise AuthenticationFailed()
        assert isinstance(instance, User)
        token, _ = Token.objects.get_or_create(user=instance)
        return {"token": token.key}


