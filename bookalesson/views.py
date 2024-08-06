
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect, reverse

from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
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

def comment_edit(request, slug, comment_id):
    """
    View to edit comments
    """
    post = get_object_or_404(Lesson, slug=slug)
    comment = get_object_or_404(CommentOnLesson, pk=comment_id)
    lesson_dates = LessonDate.objects.filter(lesson=post)  

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST, instance=comment, lesson_dates=lesson_dates)

        if comment_form.is_valid() and comment.author == request.user:
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.approved = False
            comment.save()
            messages.success(request, 'Comment updated successfully!')
            return redirect(reverse('lessons_detail', args=[slug]))
        else:
            messages.error(request, 'Error updating comment! Please ensure all fields are correctly filled.')
    else:
        comment_form = CommentForm(instance=comment, lesson_dates=lesson_dates)

    context = {
        'comment_form': comment_form,
        'lesson': post,
        'comment': comment,
    }
    return render(request, 'lesson_details.html', context)

def comment_delete(request, slug, comment_id):
    """
    View to delete a comment.
    """
    # Retrieve the Lesson and Comment instances
    post = get_object_or_404(Lesson, slug=slug)
    comment = get_object_or_404(CommentOnLesson, pk=comment_id)

    # Check if the current user is the author of the comment
    if comment.author == request.user:
        comment.delete()
        messages.success(request, 'Comment deleted successfully!')
    else:
        messages.error(request, 'You can only delete your own comments!')

    # Redirect to the post detail page
    return redirect(reverse('lessons_detail', args=[slug]))