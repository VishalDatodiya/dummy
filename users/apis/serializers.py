import re
from rest_framework import serializers

from django.contrib.auth import authenticate

from users.models import User

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")    
        user = authenticate(self, username=username, password=password)
        data["user"] = user
        return data


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=20)
    new_password1 = serializers.CharField(max_length=20)
    new_password2 = serializers.CharField(max_length=20)
    
    # def validate(self, data):
    #     old_password = data.get("old_password")
    #     new_password1 = data.get("new_password1")
    #     new_password2 = data.get("new_password2")

        # if new_password1 != new_password2:
        #     raise serializers.ValidationError(
        #                 "password must match. Please update your password."
        #             )
        # if old_password == new_password1:
        #     raise serializers.ValidationError(
        #                 "Your old password and new password are same. Please update your password."
        #             )
        # return data

class ResetPasswordSerializer(serializers.Serializer):
    new_password1 = serializers.CharField(max_length=20)
    new_password2 = serializers.CharField(max_length=20)
    
    def validate(self, data):
        new_password1 = data.get("new_password1")
        new_password2 = data.get("new_password2")

        if new_password1 != new_password2:
            raise serializers.ValidationError(
                        "password must match. Please update your password."
                    )
        return data
    
from common import utils
class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ["id", "username", "role"]

    def get_id(self, obj):
        return utils.encode(obj.id)
    
    def get_role(self, obj):
        group = obj.groups.first()
        return group.name if group else None
    
    

class AddUserSeralizer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField(max_length=100)
    role = serializers.CharField(max_length=100)
    password1 = serializers.CharField(max_length=20)
    password2 = serializers.CharField(max_length=20)
