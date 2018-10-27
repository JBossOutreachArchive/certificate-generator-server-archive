from django.core.exceptions import ObjectDoesNotExist

from rest_framework import permissions


class CanIssueCertificate(permissions.BasePermission):
    @classmethod
    def has_permission(cls, request, view):
        user = request.user
        if user:
            try:
                return user.user_permissions.get(codename='can_issue_certificate')
            except ObjectDoesNotExist:
                pass
        return False
