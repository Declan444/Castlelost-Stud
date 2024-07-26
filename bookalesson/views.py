from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Lessons


# Create your views here.
class LessonTypesList(generic.ListView):
    queryset = Lessons.objects.all()
    template_name = 'bookalesson/index.html'


def lessons_detail(request, slug):
    

    queryset = Lessons.objects.all()
    lesson = get_object_or_404(queryset, slug=slug)

    return render(
        request,
        "bookalesson/lessons_detail.html",
        {"lessons": lesson},
    )
    
