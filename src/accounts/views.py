from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CompanySerializer, JobSeekerSerializer
from .tokens import create_jwt_pair


class CompanyCreateView(CreateAPIView):
    serializer_class = CompanySerializer
    permission_classes = [AllowAny]

    def post(self, request: Request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()

            response = {
                "message": "Company account created successfully",
                "data": serializer.data
            }

            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


company_create_view = CompanyCreateView.as_view()


class JobSeekerCreateView(CreateAPIView):
    serializer_class = JobSeekerSerializer
    permission_classes = [AllowAny]

    def post(self, request: Request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()

            response = {
                "message": "Job seeker account created successfully",
                "data": serializer.data
            }

            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


job_seeker_create_view = JobSeekerCreateView.as_view()


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email)
        print(email)
        print(user)
        if user is not None:
            tokens = create_jwt_pair(user)
            response = {
                "message": "Login successfully",
                "tokens": tokens
            }

            return Response(data=response, status=status.HTTP_200_OK)

        return Response(data={"message": "Invalid email or password"})


login_view = LoginView().as_view()
