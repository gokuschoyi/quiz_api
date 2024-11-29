from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .serializer import CustomUserSerializer, LoginSerializer

# Create your views here.


@api_view(["POST"])
def signup(request):
    print("Request data", request.data)
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        # print(serializer.validated_data)
        user = serializer.save()
        return Response(
            {"message": "User created successfully", "status": serializer.data}, status=status.HTTP_201_CREATED
        )
    elif serializer.errors:
        print(serializer.errors)
        return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def login(request):
    login_serializer = LoginSerializer(data=request.data)
    print("Request data", request.data)
    print("Login serializer", login_serializer)
    if login_serializer.is_valid():
        # print(login_serializer.validated_data)
        try:
            user = CustomUser.objects.get(email=login_serializer.validated_data["email"])
            # print("User", user.id)

            if user.password != login_serializer.validated_data["password"]:
                return Response({"message": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "login success", "user_id": user.id}, status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    elif login_serializer.errors:
        # print('ERRORS',login_serializer.errors)
        return Response({"message": login_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
