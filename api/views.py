from django.contrib.auth.models import User

from rest_framework_jwt.utils import (
    jwt_payload_handler as jwtPayloadHandler,
    jwt_encode_handler as jwtEncodeHandler
)

from rest_framework.response import Response
from rest_framework import (
    generics,
    permissions,
    status
)
from api import (
    models,
    serializers,
    permissions as custom_permissions,
)

class Register(generics.CreateAPIView):
    permission_classes = []
    authentication_classes = []
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
            userData.username = reqData["name"]
            userData.save()

            payload = jwtPayloadHandler(userData)
            token = jwtEncodeHandler(payload)

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
