from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic

from .models import Lesson, CommentOnLesson, LessonDate 
from .forms import CommentForm





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
    lesson = get_object_or_404(Lesson, slug=slug)
    lesson_dates = LessonDate.objects.filter(lesson=lesson).order_by('date', 'start_time')
    
    # Check if the user has already commented on this lesson
    existing_comment = None
    if request.user.is_authenticated:
        existing_comment = CommentOnLesson.objects.filter(
            author=request.user,
            lesson_type=lesson
        ).first()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST, lesson_dates=lesson_dates)
        if comment_form.is_valid():
            # Check if the user has already submitted a comment for this lesson date
            lesson_date = comment_form.cleaned_data['lesson_date']
            if CommentOnLesson.objects.filter(
                author=request.user,
                lesson_type=lesson,
                lesson_date=lesson_date
            ).exists():
                comment_form.add_error(None, "You have already submitted a comment for this lesson on this date.")
            else:
                # Save the new comment
                comment = comment_form.save(commit=False)
                comment.author = request.user
                comment.lesson_type = lesson
                comment.save()
                return redirect('lessons_detail', slug=slug)  # Redirect after POST to avoid resubmission
    else:
        comment_form = CommentForm(lesson_dates=lesson_dates)

    comments = CommentOnLesson.objects.filter(lesson_type=lesson).order_by("-created_on")
    comment_count = comments.filter(approved=True).count()

    return render(
        request,
        "bookalesson/lessons_detail.html",
        {
            "lesson": lesson,
            "comments": comments,
            "comment_count": comment_count,
            "comment_form": comment_form,
            "existing_comment": existing_comment,
        },
    )