from django.urls import path
from auth.views import (
    ObtainJWT,
    RefreshJWT
)

urlpatterns = [
    path('api-token-auth/', ObtainJWT.as_view()),
    path('api-token-refresh/', RefreshJWT.as_view()),
]
