from django.test import TestCase
from .models import Organization, Student
from django.contrib.auth.models import User


class OrganizationTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username="jbossAdmin", password="jbossAdminsPassword")
        Organization.objects.create(user=user, name="JBoss Outreach")

    def test_if_organization_was_created(self):
        user = User.objects.get(username="jbossAdmin")
        org = Organization.objects.get(user=user)

        self.assertEqual(org.name, "JBoss Outreach")

class StudentTestcase(TestCase):
    def setUp(self):
        user = User.objects.create(username="jbossStudent", password="jbossStudentsPassword")
        Student.objects.create(user=user, name="Saba Khukhunashvili")

    def test_if_student_was_created(self):
        user = User.objects.get(username="jbossStudent")
        student = Student.objects.get(user=user)

        self.assertEqual(student.name, "Saba Khukhunashvili")
        self.assertEqual(student.email_validated, False)
