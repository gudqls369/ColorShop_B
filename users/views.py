from django.shortcuts import render
from django.contrib.auth.hashers import check_password
from django.contrib.auth.views import PasswordResetView
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,)
from users.serializers import UserSerializer,CustomTokenObtainPairSerializer, ChangePasswordSerializer, ProfileSerializer
from users.models import User

# Create your views here.
class UserView(APIView):  
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"가입완료!"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
class MockView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        user = request.user
        user.is_admin = True
        user.save()
        return Response("get")

class ChangePasswordView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = ChangePasswordSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    #비밀번호 인증
    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)

        if check_password(request.data, user.password):
            print(request.data)
            print(user.password)
            return Response({"message":"인증이 완료되었습니다."}, status=status.HTTP_200_OK)        
        else:
            return Response({"message":"맞는 비밀번호를 적어주세요."}, status=status.HTTP_400_BAD_REQUEST)

    #비밀번호 변경
    def put(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        if user == request.user:
            serializer = ChangePasswordSerializer(user, data=request.data, context={'request': request}) #request를 serializer로 넘김
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"비밀번호 변경이 완료되었습니다! 다시 로그인해주세요."} , status=status.HTTP_201_CREATED)
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":"접근 권한 없음"}, status=status.HTTP_403_FORBIDDEN)

class ProfileView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = ProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        if request.user == user:
            serializer = ProfileSerializer(user, data=request.data)
            print(request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                print(serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('권한이 없습니다', status=status.HTTP_403_FORBIDDEN)
    
    def delete(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        if request.user == user:
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response('권한이 없습니다', status=status.HTTP_403_FORBIDDEN)