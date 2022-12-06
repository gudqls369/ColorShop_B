from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from users.models import User
import re



class UserSerializer(serializers.ModelSerializer):

    password_check= serializers.CharField(error_messages={"write_only":True,'required':'비밀번호 확인까지 입력해 주세요.', 
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
        username = validated_data.get("username")
        username_reg =r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{1,20}$"
        password_reg = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"
        password = validated_data.get("password")
        password_check = validated_data.get("password_check")
       
       
        

        
        if not re.search(username_reg, str(username)) :
            raise serializers.ValidationError(detail={"username":"최소 한 개의 영문자와 숫자를 포함해 20글자 이하의 유저이름을 만들어주세요."})

    
        if not re.search(password_reg, str(password)) :
            raise serializers.ValidationError(detail={"password":"최소 한 개의 영문자와 숫자를 포함해 8글자 이상으로 만들어 주세요."})
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




class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod 
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token