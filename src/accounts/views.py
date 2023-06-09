from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CompanySerializer, JobSeekerSerializer, UserSerializer
from .tokens import create_jwt_pair


@api_view(["POST"])
@permission_classes([AllowAny])
def create_company(request: Request):
    """
    Register new company account
    :param request:
    :return company:
    """
    data = request.data
    serializer = CompanySerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        response = {
            "message": "Company account created successfully",
            "data": serializer.data
        }
        return Response(data=response, status=status.HTTP_201_CREATED)

    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
@transaction.atomic
def create_job_seeker(request: Request):
    """
    Register new job seeker account
    :param request:
    :return job_seeker:
    """
    data = request.data
    serializer = JobSeekerSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        response = {
            "message": "Job seeker account created successfully",
            "data": serializer.data
        }
        return Response(data=response, status=status.HTTP_201_CREATED)

    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)

        if user is not None:
            tokens = create_jwt_pair(user)
            response = {
                "message": "Login successfully",
                "tokens": tokens
            }

            return Response(data=response, status=status.HTTP_200_OK)

        return Response(data={"message": "Invalid email or password"})


login_view = LoginView().as_view()
