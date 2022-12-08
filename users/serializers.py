from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        user = super().create(validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user
    
    def update(self, validated_data):
        user = super().update(validated_data)
        password = user.password
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
        password = data.get("password")
        repassword = data.get("repassword")
        print(data)
        print(oldpassword)
        print(password)
        print(repassword)

        if check_password(password, oldpassword):
            print(oldpassword)
            print(password)
            raise serializers.ValidationError(detail={"password":"현재 사용중인 비밀번호와 동일한 비밀번호는 입력할 수 없습니다."})
        
        if password != repassword:
            raise serializers.ValidationError(detail={"password":"비밀번호가 일치하지 않습니다."})
        
        return data

    def update(self, instance, validated_data):
        instance.passowrd = validated_data.get('password', instance.password)
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

