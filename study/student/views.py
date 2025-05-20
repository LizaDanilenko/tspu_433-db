from django.shortcuts import render
from django.http import HttpResponse
from student.models import Group, Faculty, Student

# Create your views here.
def detail(request):
    faculties = Faculty.object.all()
    print(faculties)



    return HttpResponse("You're looking at ...")