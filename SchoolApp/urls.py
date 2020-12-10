from django.contrib import admin
from django.urls import path, include

from SchoolApp import views

urlpatterns = [
    path('api/login', views.UserLogin.as_view(), name='login'),
    path('api/signup', views.UserSignUp.as_view(), name='signup'),
    path('api/user', views.UserInfo.as_view(), name='user'),
    path('api/users', views.UserList.as_view(), name='users'),
    path('api/fee', views.FeeRecords.as_view(), name='fee'),
    path('api/assignment', views.Assignments.as_view(), name='assignment'),
]