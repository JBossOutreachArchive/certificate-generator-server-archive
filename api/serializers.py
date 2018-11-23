from django.contrib.auth.models import User
from django.conf import settings
from rest_framework import serializers
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from requests.exceptions import HTTPError
from social_django.utils import psa


from api import models

class UserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class StudentBasicSerializer(serializers.ModelSerializer):
    user = UserBasicSerializer()

    class Meta:
        model = models.Student
        fields = ('id', 'name', 'user')

    @classmethod
    def create(self, data):
        user_data = data.pop('user')
        user = UserBasicSerializer.create(UserBasicSerializer(), user_data)

        return models.Student.objects.create(user=user, name=data.pop('name'))


class OrganisationBasicSerializer(serializers.ModelSerializer):
    user = UserBasicSerializer()

    class Meta:
        model = models.Organization
        fields = ('name', 'user')

    @classmethod
    def create(self, data):
        user_data = data.pop('user')
        user = UserBasicSerializer.create(UserBasicSerializer(), user_data)

        return models.Organization.objects.create(user=user, name=data.pop('name'))


class UserOrganizationBasicSerializer(serializers.ModelSerializer):
    organization = OrganisationBasicSerializer()

    class Meta:
        model = User
        fields = ('username', 'email', 'organization')

class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Certificate
        fields = ('issued_for', 'student', 'issuing_organization')

class CertificateDetailSerializer(CertificateSerializer):
    student = StudentBasicSerializer()
    issuing_organization = OrganisationBasicSerializer()

    class Meta:
        model = models.Certificate
        fields = ('id', 'issued_for', 'student', 'issuing_organization')

class SocialSerializer(serializers.Serializer):
    access_token = serializers.CharField(
        allow_blank=False,
        trim_whitespace=True,
    )     

@api_view(http_method_names=['POST'])
@permission_classes([AllowAny])
@psa()
def exchange_token(request, backend):
    serializer = SocialSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        try:
            nfe = settings.NON_FIELD_ERRORS_KEY
        except AttributeError:
            nfe = 'non_field_errors'

        try:
            user = request.backend.do_auth(serializer.validated_data['access_token'])
        except HTTPError as e:
            return Response(
                {'errors': {
                    'token': 'Invalid token',
                    'detail': str(e),
                }},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user:
            if user.is_active:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key})
            else:
                return Response(
                    {'errors': {nfe: 'This user account is inactive'}},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {'errors': {nfe: "Authentication Failed"}},
                status=status.HTTP_400_BAD_REQUEST,
            )   
