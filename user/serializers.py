from django.core.validators import MinLengthValidator
from rest_framework import serializers
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from .models import User
from .validators import letter_validator, number_validator, special_char_validator


class InputRegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    phone_number = serializers.CharField(
        validators=[
            number_validator,
            letter_validator,
            special_char_validator,
            MinLengthValidator(limit_value=11),
        ],
        max_length=11,
    )
    email = serializers.EmailField()
    password = serializers.CharField(max_length=255)
    confirm_password = serializers.CharField(max_length=255)

    def validate_phone_number(self, phone_number):
        if User.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError("This phone number is exist")
        return phone_number

    def validate(self, data):
        if not data.get("password") or not data.get("confirm_password"):
            raise serializers.ValidationError(
                "Please fill password and confirm password"
            )

        if data.get("password") != data.get("confirm_password"):
            raise serializers.ValidationError(
                "confirm password is not equal to password"
            )
        return data


class OutPutRegisterSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField("get_token")

    class Meta:
        model = User
        fields = ("phone_number", "token", "created_at", "updated_at")

    def get_token(self, user):
        data = dict()
        token_class = RefreshToken

        refresh = token_class.for_user(user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return data
