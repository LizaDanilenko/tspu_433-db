from django.contrib import admin
from django.urls import path
from student.views import detail

urlpatterns = [
    path('', detail),
]
