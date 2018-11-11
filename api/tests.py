from django.test import TestCase
from jwt import decode
from decouple import config

from django.test import Client
c = Client()

# Create your tests here.

class TestIssuer(TestCase):
    def create_cert_issuable_user(self):
        # Create user and test is JWT is valid
        req = c.post("/api/register",data={
            "name":"test-admin",
            "password":"EY#ubuMk!kFd966%",
            "canIssue":True
        })
        self.assertEqual(req.status_code,200)
        self.assertEqual(req["Content-Type"],'application/json')
        data = req.json()
        print(data)
        self.assertEqual(data["error"],False)
        self.assertEqual(data["message"],"User test-admin has been successfully created.")
        tokenData = decode(data["jwt"],config("SECRET_KEY"),
            algorithms=["HS256"],
            issuer="JBoss-certificate-generator",
            audience="JBoss-certificate-generator"
        )
        print(tokenData)
        self.assertEqual(tokenData["name"],"test-admin")
        self.assertEqual(tokenData["canIssue?"],'True')
        self.assertEqual(tokenData["user_id"],1)
    def authenticate_cert_issuable_user(self):
        # Authenticate user and obtain JWT
        tokenReq = c.post("/api-token-auth/",data={
            "username":"test-admin",
            "password":"EY#ubuMk!kFd966%"
        })
        self.assertEqual(tokenReq.status_code,200)
        token = tokenReq.json()["token"]
        tokenData = decode(token,config("SECRET_KEY"),
            algorithms=["HS256"]
        )
        print(tokenData)
        self.assertEqual(tokenData["username"],"test-admin")
        self.assertEqual(tokenData["user_id"],1)
    def test(self):
        # Run tests in correct order
        self.create_cert_issuable_user()
        self.authenticate_cert_issuable_user()
class TestStudent(TestCase):
    def create_cert_student_user(self):
        # Create user and test is JWT is valid
        req = c.post("/api/register",data={
            "name":"test-student",
            "password":"9ggz&;K-ebC!%R3c",
            "canIssue":False
        })
        self.assertEqual(req.status_code,200)
        self.assertEqual(req["Content-Type"],'application/json')
        data = req.json()
        print(data)
        self.assertEqual(data["error"],False)
        self.assertEqual(data["message"],"User test-student has been successfully created.")
        tokenData = decode(data["jwt"],config("SECRET_KEY"),
            algorithms=["HS256"],
            issuer="JBoss-certificate-generator",
            audience="JBoss-certificate-generator"
        )
        print(tokenData)
        self.assertEqual(tokenData["name"],"test-student")
        self.assertEqual(tokenData["canIssue?"],'False')
        self.assertEqual(tokenData["user_id"],1)
    def authenticate_cert_student_user(self):
        # Authenticate user and obtain JWT
        tokenReq = c.post("/api-token-auth/",data={
            "username":"test-student",
            "password":"9ggz&;K-ebC!%R3c"
        })
        self.assertEqual(tokenReq.status_code,200)
        token = tokenReq.json()["token"]
        tokenData = decode(token,config("SECRET_KEY"),
            algorithms=["HS256"]
        )
        print(tokenData)
        self.assertEqual(tokenData["username"],"test-student")
        self.assertEqual(tokenData["user_id"],1)
    def test(self):
        # Run tests in correct order
        self.create_cert_student_user()
        self.authenticate_cert_student_user()