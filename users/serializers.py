from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from users.models import User
import re

class UserSerializer(serializers.ModelSerializer):
    password_check= serializers.CharField(write_only=True, error_messages={'required':'비밀번호 확인까지 입력해 주세요.', 
    'blank':'비밀번호 확인까지 입력해 주세요.'}) 

    class Meta:
        model = User
        fields = ("username","nickname","password", "password_check")
        extra_kwargs = {
            "username" :{"error_messages" : {
                "required" : "유저이름을 입력해 주세요.",
                "blank" : "유저이름을 입력해 주세요."}},
            "nickname" : {"error_messages":{
                "required":"닉네임을 입력해 주세요.",
                "blank":"닉네임을 입력해 주세요."}},
            "password" : {"write_only":True,
                          "error_messages":{
                "required":"비밀번호를 입력해 주세요.",
                "blank":"비밀번호를 입력해 주세요."}},
        }

    def validate(self, validated_data) :
        password_reg = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
        password = validated_data.get("password")
        password_check = validated_data.get("password_check")

        if not re.search(password_reg, str(password)) :
            raise serializers.ValidationError(detail={"password":"비밀번호는 최소 한 개 이상의 영문자, 숫자, 특수문자를 포함해 8글자 이상으로 만들어 주세요."})
        elif password != password_check :
            raise serializers.ValidationError(detail={"password":"동일한 비밀번호를 입력해 주세요."})

        return validated_data

    def create(self, validated_data):
        username = validated_data["username"]
        nickname = validated_data["nickname"]
        password = validated_data["password"]
        user = User(
            username = username,
            nickname=nickname,
            password = password
            )
        user.set_password(password)
        user.save()
        return user
    
    def update(self, validated_data):
        username = validated_data["username"]
        nickname = validated_data["nickname"]
        password = validated_data["password"]
        user = User(
            username=username,
            nickname=nickname,
            password = password
            )
        user.set_password(password)
        user.save()
        return user

class ChangePasswordSerializer(serializers.ModelSerializer):
    repassword = serializers.CharField(error_messages=
    {"write_only":True, 
    "required":"비밀번호 확인까지 입력해주세요",
    'blank':'비밀번호를 입력해주세요.'})
    
    class Meta:
        model = User
        fields = ("password", "repassword")
        extra_kwargs = {
            "password" : 
            {"write_only":True,
            "error_messages":
            {"required":"비밀번호를 입력해 주세요.",
            "blank":"비밀번호를 입력해 주세요."}},
        }
    
    def validate(self, data):
        oldpassword = self.context.get("request").user.password
        password_reg = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
        password = data.get("password")
        repassword = data.get("repassword")

        if check_password(password, oldpassword):
            raise serializers.ValidationError(detail={"password":"현재 사용중인 비밀번호와 동일한 비밀번호는 입력할 수 없습니다."})
        
        if not re.search(password_reg, str(password)) :
            raise serializers.ValidationError(detail={"password":"비밀번호는 최소 한 개 이상의 영문자, 숫자, 특수문자를 포함해 8글자 이상으로 만들어 주세요."})
        elif password != repassword :
            raise serializers.ValidationError(detail={"password":"동일한 비밀번호를 입력해 주세요."})
        
        return data


    def update(self, instance, validated_data):
        instance.password = validated_data.get('password', instance.password)
        instance.set_password(instance.password)
        instance.save()
        return instance

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod 
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username

        return token

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'profile_img', 'username', 'nickname', 'bio')
