from django.urls import path

from api import views

urlpatterns = [
    path('org/', views.OrganizationCreation.as_view()),
    path('org/certificates/', views.OrganizationCertificateList.as_view()),

    path('user/', views.StudentCreation.as_view()),
    path('user/<int:pk>', views.StudentDetail.as_view()),
    path('user/<username>', views.StudentDetail.as_view()),
    path('users/', views.StudentList.as_view()),

    path('get_certificates/', views.CertificateList.as_view()),
    path('certificate/<pk>', views.CertificateDetail.as_view()),

    path('issue_certificate/', views.CertificateCreate.as_view()),
]
