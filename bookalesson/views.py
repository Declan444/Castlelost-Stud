from django.shortcuts import render
from django.views import generic
from .models import Lessons


# Create your views here.
class LessonTypesList(generic.ListView):
    model = Lessons
