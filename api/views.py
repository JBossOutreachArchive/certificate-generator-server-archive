from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework import (
    generics,
    permissions,
    status
)
from rest_framework.decorators import (
    authentication_classes,
    permission_classes
)
from api import (
    models,
    serializers,
    permissions as custom_permissions,
)
from jwt import encode
from decouple import config
from datetime import datetime

@authentication_classes([])
@permission_classes([])
class Register(generics.CreateAPIView):
    @classmethod
    def post(self, req):
        try:
            reqData = req.data
            requiredParams = ["canIssue","name","password"]

            if (sorted(list(reqData.keys())) != requiredParams):
                raise Exception("Missing or invalid parameters")
            userData = (
                models.Organization()
                if reqData["canIssue"]
                else models.Student()
            )
            if User.objects.filter(username=reqData["name"]).count() == 0:
                userData.user = User.objects.create_user(reqData["name"],password=reqData["password"])
            else:
                raise Exception(f"A user with name {reqData['name']} already exists. Try a different username.")
            userData.name = reqData["name"]
            userData.save()

            token = encode({
                "name":reqData["name"],
                "canIssue?":reqData["canIssue"],
                "iat":int((datetime.utcnow()-datetime(1970,1,1)).total_seconds()),
                "nbf":int((datetime.utcnow()-datetime(1970,1,1)).total_seconds()),
                "exp":int((datetime.utcnow()-datetime(1970,1,1)).total_seconds())+3600,
                "iss":"JBoss-certificate-generator",
                "aud":"JBoss-certificate-generator",
                "user_id":userData.id
            },config("SECRET_KEY"))

            return Response({
                "error":False,
                "message":f"User {reqData['name']} has been successfully created.",
                "jwt":token
            })
        except Exception as error:
            print(error)
            return Response({
                "error":True,
                "message":str(error)
            },status=400)

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
