from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
import jwt
import csv
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework_jwt.settings import api_settings
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


class CertificateCreateFromCSV(generics.CreateAPIView):
    model = models.Certificate
    permission_classes = (custom_permissions.CanIssueCertificate,)
    serializer_class = serializers.CertificateSerializer

    def create(self, request):
        if request.method == 'POST':
            file = request.FILES["file"]
            if(not file.name.endswith(".csv") or (file.content_type != "text/csv" and file.content_type != "application/vnd.ms-excel")):
                return Response("Please only upload csv files", status=status.HTTP_400_BAD_REQUEST)
            fileData = file.read().decode("utf-8")
            csvData = list(csv.reader(fileData.split("\n")))
            csvData.pop(0)
            certificates = []
            for row in csvData:
                # First column is issued_to
                # Second column is issued_for
                if(len(row) != len(self.model.getFields())):
                    continue
                data = {
                    "student": models.Student.objects.get(user__username=row[0]).pk,
                    "issued_for": row[1],
                    "issuing_organization": request.user.organization.pk
                }
                serializer = self.serializer_class(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                certificates.append(serializer.data)
            return Response(certificates, status=status.HTTP_201_CREATED)


class StudentCreation(generics.CreateAPIView):
    model = models.Student
    serializer_class = serializers.StudentBasicSerializer
    authentication_classes = tuple()
    permission_classes = tuple()

    @classmethod
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        try:
            if serializer.is_valid(raise_exception=True):
                student = serializer.create(request.data)
                jwt_token = {
                    'token': jwt_encode_handler(jwt_payload_handler(student.user))
                }
                return Response(jwt_token, status=status.HTTP_201_CREATED)
        except IntegrityError:
            serializer.error_messages = {
                'Error': 'Student with that username already exists!'}
        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)


class OrganizationCreation(generics.CreateAPIView):
    model = models.Organization
    serializer_class = serializers.OrganisationBasicSerializer
    authentication_classes = tuple()
    permission_classes = tuple()

    @classmethod
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        try:
            if serializer.is_valid(raise_exception=True):
                user = serializer.create(request.data)
                jwt_token = {'token': jwt.encode(
                    serializer.data, config('SECRET_KEY'))}
                return Response(jwt_token, status=status.HTTP_201_CREATED)
        except IntegrityError:
            serializer.error_messages = {
                'Error': 'Organization with that username already exists!'}
        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)


class StudentDetail(generics.RetrieveAPIView):
    queryset = models.Student.objects.all()
    model = models.Student
    get_object_using = 'user__username'
    serializer_class = serializers.StudentBasicSerializer

    permission_classes = (permissions.IsAdminUser,)

    def get_object(self):
        if 'pk' in self.kwargs:
            return super(StudentDetail, self).get_object()

        filter_kwargs = {
            self.get_object_using: self.kwargs['username']
        }
        obj = get_object_or_404(self.model, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj


class StudentList(generics.ListAPIView):
    queryset = models.Student.objects.all()
    model = models.Student
    serializer_class = serializers.StudentBasicSerializer

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
