from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic

from .models import Lesson 





# Create your views here.
class LessonList(generic.ListView):
    model = Lesson
    template_name = 'bookalesson/index.html'
    context_object_name = 'lessons_list'

    def get_queryset(self):
        return Lesson.objects.all

#def lesson_list(request):
#    lessons = Lesson.objects.all()
#    return render(request, 'bookalesson/index.html', {'lesson_list': lessons})

def lessons_detail(request, slug):
    
    queryset = Lesson.objects.all()
    lesson = get_object_or_404(queryset, slug=slug)
    comments = lesson.comments.all().order_by("-created_on")
    comment_count = lesson.comments.filter(approved=True).count()
    return render(
        request,
        "bookalesson/lessons_detail.html",
        {
            "lesson": lesson,
            "comments": comments,
            "comment_count": comment_count,
         
         },
    )
