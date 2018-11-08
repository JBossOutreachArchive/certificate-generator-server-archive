from django.contrib.auth.models import User
from rest_framework import serializers

from api import models


class StudentBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Student
        fields = ('name',)

    def create(self, data):
        user_data = data.pop('user')
        user = UserBasicSerializer.create(UserBasicSerializer(), user_data)

        return models.Student.objects.create(user=user, name=data.pop('name'))


class UserBasicSerializer(serializers.ModelSerializer):
    student = StudentBasicSerializer()

    class Meta:
        model = User
        fields = ('username', 'email', 'student')


class OrganisationBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Organization
        fields = ('name',)

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
