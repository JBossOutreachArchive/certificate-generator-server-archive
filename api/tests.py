import json
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.test import (
    APIRequestFactory,
    APIClient
)
from api import (
    models,
    views
)


class StudentRegistrationTestcase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()

    def test_if_student_was_create(self):
        # Registering a new user
        payload = {
            "name": "test",
            "user": {
                "username": "test",
                "password": "password",
                "email": "test@test.com"
            }
        }
        request = self.factory.post('/api/user', payload, format='json')
        response = views.StudentCreation.as_view()(request)
        self.assertEqual(response.status_code, 201)

        # Checking whether the actual user object was created or not
        user = User.objects.get(username='test')
        self.assertEqual(user.username, 'test')
        self.assertEqual(user.email, 'test@test.com')

        # Checking if password is stored as a hash or plain
        user = User.objects.get(username='test')
        self.assertNotEqual(user.password, "password")

        # Trying a login protected route for student
        payload = {
            "username": "test",
            "password": "password"
        }
        request = self.factory.post('/api-token-auth/', payload, format='json')
        response = obtain_jwt_token(request)
        self.assertEqual(response.status_code, 200)
        response.render()
        token = json.loads(response.content)['token']
        self.client.credentials(HTTP_AUTHORIZATION='JWT {}'.format(token))
        response = self.client.get('/api/get_certificates/')
        self.assertEqual(response.status_code, 200)
