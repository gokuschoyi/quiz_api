from django.contrib.auth.hashers import make_password, check_password
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .serializer import CustomUserSerializer, LoginSerializer


@api_view(["POST"])
def signup(request):
    print("Request data", request.data)
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
        user = serializer.save()
        return Response(
            {"message": "User created successfully"}, status=status.HTTP_201_CREATED
        )
    elif serializer.errors:
        print(serializer.errors)
        return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login(request):
    login_serializer = LoginSerializer(data=request.data)
    if login_serializer.is_valid():
        try:
            user = CustomUser.objects.get(email=login_serializer.validated_data["email"])

            if not check_password(login_serializer.validated_data["password"], user.password):
                return Response({"message": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "login success", "user_id": user.id, "email":user.email, "first_name":user.first_name}, status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    elif login_serializer.errors:
        return Response({"message": login_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
