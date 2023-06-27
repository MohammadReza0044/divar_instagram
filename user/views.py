from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import InputRegisterSerializer, OutPutRegisterSerializer


class RegisterApi(APIView):
    def post(self, request):
        serializer = InputRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.create(
                phone_number=serializer.validated_data.get("phone_number"),
                password=make_password(serializer.validated_data["password"]),
                first_name=serializer.validated_data.get("first_name"),
                last_name=serializer.validated_data.get("last_name"),
                email=serializer.validated_data.get("email"),
            )

        except Exception as ex:
            return Response(f"Database Error {ex}", status=status.HTTP_400_BAD_REQUEST)
        return Response(
            OutPutRegisterSerializer(user, context={"request": request}).data
        )
