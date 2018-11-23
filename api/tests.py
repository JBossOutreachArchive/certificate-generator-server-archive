from contextlib import contextmanager
import json
import re
import responses
import get_current_site
from urllib.parse import urlparse, parse_qs
from rest_framework.test import APITestCase
from social_core.backends import google, facebook, twitter
from requests.exceptions import HTTPError
from requests.models import Response
from core.models import User
import core.tests.fixtures as fixtures
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

SOCIAL_URL = get_current_site(request)

class TryToken:  

    def try_token(self, token):
        return self.post(
            SOCIAL_URL.format(self.provider),
            data={'access_token': token},
        )


class TestInvalidProvider(TryToken, APITestCase):

    provider = 'google'
    def test_only_allowed_backends_work(self):
        for token in USER_INFO:
            with self.subTest(token=token):
                resp = self.try_token(token)
                self.assertEqual(resp.status_code, 404)

USER_INFO = {  # Example
    'user_1': {
        'id': '007',
        'name': 'Sai Vittal B',
        'email': 'saivittalb@gmail.com',
    },
}


def respond_to(request):

    token = parse_qs(urlparse(request.url).query)['access_token'][0]
    status = 200
    try:
        body = USER_INFO[token]
    except KeyError:
        body = {'errors': 'Invalid Token'}
        status = 401
    return (status, {}, json.dumps(body))


@contextmanager
def mocked(endpoint):

    with responses.RequestsMock() as rsps:
        rsps.add_callback(responses.GET, endpoint,
                          callback=respond_to,
                          content_type='application/json',
                          match_querystring=True,
                          )
        yield rsps


class SocialAuthTests(TryToken):

    def test_new_user_creation(self):
        for token, data in USER_INFO.items():
            with self.subTest(token=token), mocked(self.mock_url):
                resp = self.try_token(token)
                self.assertEqual(self.status_head(resp), 2)
                self.assertIn('token', resp.data)
                self.assertNotEqual(resp.data['token'], token)
                self.assertEqual(User.objects.filter(email=data['email']).count(), 1)
                user_model = User.objects.get(email=data['email'])
                self.assertEqual(user_model.username, user_model.email)

    def test_existing_user_login(self):
        for token, data in USER_INFO.items():
            
            User.objects.create_user(data['email'], email=data['email'],
                                     first_name=data['name'], last_name='')

            with self.subTest(token=token), mocked(self.mock_url):
                resp = self.try_token(token)
                self.assertEqual(self.status_head(resp), 2)
                self.assertIn('token', resp.data)
                self.assertNotEqual(resp.data['token'], token)
                self.assertEqual(User.objects.filter(email=data['email']).count(), 1)
                user = User.objects.get(email=data['email'])
                self.assertEqual(user.get_full_name(), data['name'])

    def test_invalid_social_token(self):

        usernames = {u.username for u in User.objects.all()}
        token = 'invalid_token' 
        resp = self.try_token(token)
        self.assertEqual(self.status_head(resp), 4)
        self.assertNotIn('token', resp.data)
        new_usernames = {u.username for u in User.objects.all()}
        self.assertEqual(usernames, new_usernames)

QUERY_STRINGS_RE = '\?([\w-]+(=[\w-]*)?(&[\w-]+(=[\w-]*)?)*)?$' #Regular expression string designed for query strings from the end of an URL.

class TestGoogle(SocialAuthTests, APITestCase):
    provider = 'google-oauth2'
    base_url = 'https://www.googleapis.com/plus/v1/people/me'.replace('.', r'\.')
    mock_url = re.compile(
        base_url + QUERY_STRINGS_RE
    )

class TestFacebook(SocialAuthTests, APITestCase):
    provider = 'facebook'
    base_url = facebook.FacebookOAuth2.USER_DATA_URL.replace('.', r'\.')
    mock_url = re.compile(
        base_url + QUERY_STRINGS_RE
    )

class TestTwitter(SocialAuthTests, APITestCase):
    provider = 'twitter'
    base_url = twitter.TwitterOAuth2.USER_DATA_URL.replace('.', r'\.')
    mock_url = re.compile(
        base_url + QUERY_STRINGS_RE
    )    
