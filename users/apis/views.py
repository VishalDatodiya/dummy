from django.contrib.auth.models import Group
from django.db.models import Q

from django.contrib.auth.hashers import check_password

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema

from lms_indeed.settings import SIMPLE_JWT

from users.apis.serializers import LoginSerializer, ChangePasswordSerializer, AddUserSeralizer, ResetPasswordSerializer, UserSerializer
from users.models import User

from common import responses
from common.permissions import IsSuperUser

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        "access_time_limit" : SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
    }

class LoginView(APIView):

    """Login using username and password and generating the JWT tokens. access_token time limit is 5 minutes."""
    @extend_schema(request=LoginSerializer)
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        if user:
            token = get_tokens_for_user(user)
            response_data = responses.login_success_response(token)
            return Response(response_data, status=status.HTTP_200_OK)
        response_data = responses.login_failed_response()
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    """ 
        It takes 3 values. Old password, new password and confirmation password.
        First check old password than set the new password
    """

    permission_classes = [IsAuthenticated]

    @extend_schema(request=ChangePasswordSerializer)
    def post(self, request, *args, **kwargs):
        serializers = ChangePasswordSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        user = request.user
        user = User.objects.get(username=user.username)
        if not check_password(serializers.data["old_password"], user.password):
            response_data = responses.invalid_password_response()
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        if serializers.data["old_password"] == serializers.data["new_password1"]:
            response_data = responses.old_and_new_password_same_response()
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        if serializers.data["new_password1"] != serializers.data["new_password2"]:
            response_data = responses.password_mismatched_response()
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        if user:
            user.set_password(serializers.validated_data["new_password1"])
            user.save()
            response_data = responses.password_successfully_changed_response()
            return Response(response_data, status=status.HTTP_200_OK)
        
        response_data = responses.failed_response()
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
    
from common import utils
class ResetPasswordView(APIView):
    
    """
        Only admin can change the password.
        Id will get encrypted so decoded first.
    """
    
    permission_classes = [IsAuthenticated, IsSuperUser]
    
    def post(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id', None)
        try:
            user_id = utils.decode(user_id)
        except:
            return Response({"error":"Wrong user id"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(id=user_id)
        if user:
            user.set_password(serializer.validated_data["new_password1"])
            user.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response("Something went wrong.", status=status.HTTP_400_BAD_REQUEST)


class TokenRefreshView(APIView):
    """
        It will regenrate the access token from the refresh token.
    """

    permission_classes = [IsAuthenticated]
    def post(self, request):
        refresh_token = request.data.get("refresh")
        if refresh_token:
            try:
                refresh_token_obj = RefreshToken(refresh_token)
                access_token = str(refresh_token_obj.access_token)

                return Response({"access": access_token}, status=status.HTTP_200_OK)
            except Exception as e:
                response_data = responses.refresh_token_invalid()
                return Response(response_data ,status=status.HTTP_401_UNAUTHORIZED)
        else:
            response_data = responses.refresh_token_required_response()
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

class UserlistingView(APIView):

    def get(self, request, *args, **kwargs):
        role = request.query_params.get('role', None)
        # name = request.query_params.get('name', None)
        
        if role:
            users = User.objects.filter(
                Q(groups__name=role))
        else:
            users = User.objects.all()
        user_serializer = UserSerializer(users, many=True).data
        return Response(user_serializer, status=status.HTTP_200_OK)


class AddUserView(APIView):
    """Add a user and getting role from the Group model"""

    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        seralizer = AddUserSeralizer(data=request.data)
        seralizer.is_valid(raise_exception=True)

        user = User.objects.filter(username=seralizer.data["name"])
        if user.exists():
            response_data = responses.user_already_created_response()
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        
        try:
            user = User.objects.create(
                username=seralizer.data["name"],
                email = seralizer.data["email"],
            )
            my_group = Group.objects.get(name=seralizer.data["role"]) 
            my_group.user_set.add(user)
            
            user.set_password(seralizer.data["password1"])
            user.save()

            response_data = responses.user_created_response()
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception:
            response_data = responses.failed_response()
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

