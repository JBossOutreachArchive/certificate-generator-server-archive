from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework import (
    generics,
    permissions
)
from api import (
    models,
    serializers,
    permissions as custom_permissions,
)


class StudentDetail(generics.RetrieveAPIView):
    queryset = User.objects.exclude(student = None)
    model = User
    serializer_class = serializers.UserBasicSerializer

    permission_classes = (permissions.IsAdminUser,)

class StudentList(generics.ListAPIView):
    queryset = User.objects.exclude(student = None)
    model = User
    serializer_class = serializers.UserBasicSerializer

    permission_classes = (permissions.IsAdminUser,)

class CertificateList(generics.ListAPIView):
    model = models.Certificate
    serializer_class = serializers.CertificateSerializer

    def get_queryset(self):
        return models.Certificate.objects.filter(student = self.request.user.student).exclude(student = None)

class CertificateCreate(generics.CreateAPIView):
    model = models.Certificate
    permission_classes = (custom_permissions.CanIssueCertificate,)
    serializer_class = serializers.CertificateSerializer