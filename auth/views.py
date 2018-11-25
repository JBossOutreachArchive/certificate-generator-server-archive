from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import JSONWebTokenAPIView
from rest_framework_jwt.serializers import (
    JSONWebTokenSerializer,
    RefreshJSONWebTokenSerializer,
)


jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

def will_it_raise_exception(func):
    try:
        func()
        return True
    except Exception:
        return False

class JSONWebTokenAPIViewWithRoles(JSONWebTokenAPIView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, user, request)
            response_data['is_student'] = will_it_raise_exception(lambda: user.student)
            response_data['is_organization'] = will_it_raise_exception(lambda: user.organization)
            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ObtainJWT(JSONWebTokenAPIViewWithRoles):
    serializer_class = JSONWebTokenSerializer

class RefreshJWT(JSONWebTokenAPIViewWithRoles):
    serializer_class = RefreshJSONWebTokenSerializer
