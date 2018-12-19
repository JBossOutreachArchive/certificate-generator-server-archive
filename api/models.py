import uuid

from django.db import models
from django.contrib.auth.models import User, Permission
from django.core.validators import (
    ProhibitNullCharactersValidator,
)

# Create your models here.


class Organization(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100,
                            validators=[ProhibitNullCharactersValidator])

    def save(self, *args, **kwargs):
        issue_certificate_permission = Permission.objects.get(codename='can_issue_certificate')
        self.user.user_permissions.add(issue_certificate_permission)
        super(Organization, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100,
                            validators=[ProhibitNullCharactersValidator])

    # fields for account activation
    activation_key = models.CharField(max_length=255, default=1)
    email_validated = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Certificate(models.Model):
    id = models.UUIDField(unique=True, default=uuid.uuid4, primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    issuing_organization = models.ForeignKey(Organization,
                                             on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    issued_for = models.CharField(max_length=256)

    @classmethod
    def getFields(cls):
        autoGenerate = ["date", "id", "issuing_organization"]
        fields = cls._meta.get_fields()
        return [field.name for field in fields if not field.name in autoGenerate]

    class Meta:
        permissions = (
            ("can_issue_certificate", "Can Issue Certificate"),
        )
