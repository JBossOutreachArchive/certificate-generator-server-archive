from django.db import models
from django.contrib.auth.models import User
from django.core.validators import (
    ProhibitNullCharactersValidator,
)

# Create your models here.

class Organization(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    name = models.CharField(max_length = 100, validators = [ProhibitNullCharactersValidator])

    def __str__ (self):
        return self.name

    class Meta:
        permissions = (
            ("can_issue_certificate", "Can Issue Certificate"),
        )

class Student(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    name = models.CharField(max_length = 100, validators = [ProhibitNullCharactersValidator])

    # fields for account activation
    activation_key = models.CharField(max_length = 255, default = 1)
    email_validated = models.BooleanField(default = False)

    def __str__(self):
        return self.name