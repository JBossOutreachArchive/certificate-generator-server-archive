from django.urls import path

from api import views

urlpatterns = [
    path('user/<int:pk>', views.StudentDetail.as_view()),
    path('users/', views.StudentList.as_view()),
]