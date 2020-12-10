from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
import requests
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from SchoolApp.models import User, Fee, Assignment
from SchoolApp.serializer import UserSerializer, FeeSerializer, AssignmentSerializer


def get_token(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }


class UserLogin(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        req = request.data
        email = req.get('email')
        password = req.get('password')
        user = User.object.filter(email=email).first()

        if user is not None and user.check_password(password):
            token = get_token(user)
            return Response(data=token)
        return Response({'failed': 'Check email or your password.'})


class UserSignUp(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializers = UserSerializer(data=request.data)
        if serializers.is_valid():
            user = serializers.save()
            # send_activation_email(request, user)
            return Response(serializers.data, status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class UserInfo(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        email = request.GET.get('email')
        user = User.object.filter(email=email).first()

        if user:
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'failed': 'No user'})


class UserList(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        all_users = User.object.all()
        serializer = UserSerializer(all_users, many=True)
        return Response(serializer.data)


class FeeRecords(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        id = request.GET.get('id')
        user = User.object.filter(id=id).first()
        fee = Fee.objects.all().filter(user=user)

        if fee:
            serializer = FeeSerializer(fee, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'failed': 'No fee record for this student'})

    def post(self, request):
        serializers = FeeSerializer(data=request.data)
        if serializers.is_valid():
            fee = serializers.save()
            # send_activation_email(request, user)
            return Response(serializers.data, status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class Assignments(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        id = request.GET.get('id')
        user = User.object.filter(id=id).first()
        print(user.current_class)
        assignments = Assignment.objects.all().filter(current_class=user.current_class)

        if assignments:
            serializer = AssignmentSerializer(assignments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'No data':'No Assignments yet.'})

    def post(self, request):
        serializers = AssignmentSerializer(data=request.data)
        if serializers.is_valid():
            assignment = serializers.save()
            return Response(serializers.data, status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
