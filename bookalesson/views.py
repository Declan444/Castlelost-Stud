from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def my_lesson(request):
    return HttpResponse("Welcome to Castlelost Stud. Home of Holly lenahan")