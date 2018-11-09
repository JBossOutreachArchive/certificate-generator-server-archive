from django.contrib.auth.models import User
import jwt
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, permission_classes
from decouple import config

from rest_framework import (
    generics,
    permissions,
    status
)
from api import (
    models,
    serializers,
    permissions as custom_permissions
)

@authentication_classes([])
@permission_classes([])
class StudentCreation(generics.CreateAPIView):
    model = models.Student
    serializer_class = serializers.StudentBasicSerializer

    @classmethod
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.create(request.data)
                jwt_token = {'token': jwt.encode(serializer.data, config('SECRET_KEY'))}
                return Response(jwt_token, status=status.HTTP_201_CREATED)
        except:
            serializer.error_messages = {'Error': 'Student with that username already exists!'};
        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([])
@permission_classes([])
class OrganizationCreation(generics.CreateAPIView):
    model = models.Organization
    serializer_class = serializers.OrganisationBasicSerializer

    @classmethod
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        try:
            if serializer.is_valid(raise_exception=True):
                serializer.create(request.data)
                jwt_token = {'token': jwt.encode(serializer.data, config('SECRET_KEY'))}
                return Response(jwt_token, status=status.HTTP_201_CREATED)
        except:
            serializer.error_messages = {'Error': 'Organization with that username already exists!'}
        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

class StudentDetail(generics.RetrieveAPIView):
    queryset = User.objects.exclude(student=None)
    model = User
    serializer_class = serializers.UserBasicSerializer

    permission_classes = (permissions.IsAdminUser,)


class StudentList(generics.ListAPIView):
    queryset = User.objects.exclude(student=None)
    model = User
    serializer_class = serializers.UserBasicSerializer

    permission_classes = (permissions.IsAdminUser,)


class CertificateList(generics.ListAPIView):
    model = models.Certificate
    serializer_class = serializers.CertificateDetailSerializer

    def get_queryset(self):
        return models.Certificate.objects.filter(student=self.request.user.student). \
                                          exclude(student=None)


class CertificateDetail(generics.RetrieveAPIView):
    model = models.Certificate
    serializer_class = serializers.CertificateDetailSerializer

    def get_queryset(self):
        return models.Certificate.objects. \
                filter(student=self.request.user.student).exclude(student=None)


class CertificateCreate(generics.CreateAPIView):
    model = models.Certificate
    permission_classes = (custom_permissions.CanIssueCertificate,)
    serializer_class = serializers.CertificateSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['issuing_organization'] = request.user.organization.pk
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
