from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        model = get_user_model()
        # fields are going to inclode in serializer that are going to convert from/to json
        # Fields that will be accessible in the API either to read or write
        fields = ("email", "password", "name")
        # extra restrictions for the fields
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

        # method for creating the object(we are overriding it)
        def create(self, validated_data):
            """Create a new user with encrypted password and return it"""
            return get_user_model().objects.create_user(**validated_data)

        def update(self, instance, validated_data):
            """Update a user, setting the password correctly and return it"""
            password = validated_data.pop("password", None)
            user = super().update(instance, validated_data)

            if password:
                user.set_password(password)
                user.save()
            return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""

    email = serializers.CharField()
    password = serializers.CharField(style={"input_type": "password"}, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(request=self.context.get("request"), username=email, password=password)
        if not user:
            msg = _("Unable to authenticate with provided credentials")
            raise serializers.ValidationError(msg, code="authentication")

        attrs["user"] = user
        return attrs
