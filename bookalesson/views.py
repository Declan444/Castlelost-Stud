
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect

from django.views import generic
from django.contrib import messages

from .models import Lesson, CommentOnLesson, LessonDate 
from .forms import CommentForm





# Create your views here.
class LessonList(generic.ListView):
    model = Lesson
    template_name = 'bookalesson/lessons.html'
    context_object_name = 'lessons_list'

    def get_queryset(self):
        return Lesson.objects.all


def lessons_detail(request, slug):
    lesson = get_object_or_404(Lesson, slug=slug)
    
    # Show all the lesson dates for the specific user if authenticated.
    if request.user.is_authenticated:
        lesson_dates = LessonDate.objects.filter(lesson=lesson, user=request.user).order_by('date', 'start_time')
    else:
        lesson_dates = LessonDate.objects.filter(lesson=lesson).order_by('date', 'start_time')

    if request.method == 'POST':
        # check if user logged in
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to leave a comment.")
            return redirect('lessons_detail', slug=slug)
        #create form
        comment_form = CommentForm(request.POST, lesson_dates=lesson_dates)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.lesson_type = lesson
            #get lesson dates
            lesson_date = comment.lesson_date
            if lesson_date and lesson_date.user != request.user:
                # if lesson belongs to another user, show error message
                messages.error(request, "You can only comment on a lesson that you had.")
                return redirect('lessons_detail', slug=slug)
            # check if user has commented on this lesson
            if CommentOnLesson.objects.filter(
                author=request.user,
                lesson_type=lesson,
                lesson_date=lesson_date
            ).exists():
                # if commented on this lesson show message
                messages.error(request, "You have already commented on this lesson date.")
                return redirect('lessons_detail', slug=slug)
            # save comment
            comment.save()
            messages.success(request, "Your comment has been added successfully.")
            return redirect('lessons_detail', slug=slug)
    else:
        comment_form = CommentForm(lesson_dates=lesson_dates)
    # display comments in decending order
    comments = CommentOnLesson.objects.filter(lesson_type=lesson).order_by("-created_on")
    comment_count = comments.filter(approved=True).count()
    #render template
    return render(
        request,
        "bookalesson/lessons_detail.html",
        {
            "lesson": lesson,
            "lesson_dates": lesson_dates,
            "comments": comments,
            "comment_count": comment_count,
            "comment_form": comment_form,
        }
    )