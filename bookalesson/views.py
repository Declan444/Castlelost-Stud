

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import Http404
from django.utils.timezone import now
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseBadRequest
from .models import Lesson, CommentOnLesson, LessonDate, Instructor, Booking 
from .forms import CommentForm
from datetime import datetime, timedelta
import calendar
from django.contrib.auth.decorators import login_required






# Create your views here.
class LessonList(generic.ListView):
    model = Lesson
    template_name = 'bookalesson/lessons.html'
    context_object_name = 'lessons_list'

    def get_queryset(self):
        return Lesson.objects.all


def lessons_detail(request, slug):
    lesson = get_object_or_404(Lesson, slug=slug)
    
    # show all the lesson dates for the specific user if authenticated
    if request.user.is_authenticated:
        lesson_dates = LessonDate.objects.filter(lesson=lesson, user=request.user).order_by('date', 'start_time')
    else:
        lesson_dates = LessonDate.objects.filter(lesson=lesson).order_by('date', 'start_time')

    if request.method == 'POST':
        # check if user is logged in
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to leave a comment.")
            return redirect('lessons_detail', slug=slug)
        
        comment_form = CommentForm(request.POST, lesson_dates=lesson_dates)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.lesson_type = lesson
            
            lesson_date = comment.lesson_date
            if lesson_date and lesson_date.user != request.user:
               
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
            
            comment.save()
            messages.success(request, "Your comment has been added successfully.")
            return redirect('lessons_detail', slug=slug)
    else:
        comment_form = CommentForm(lesson_dates=lesson_dates)
    
    comments = CommentOnLesson.objects.filter(lesson_type=lesson).order_by("-created_on")
    comment_count = comments.filter(approved=True).count()
   
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
    # get the Lesson 
    post = get_object_or_404(Lesson, slug=slug)
    comment = get_object_or_404(CommentOnLesson, pk=comment_id)

    # check if the user authorised
    if comment.author == request.user:
        comment.delete()
        messages.success(request, 'Comment deleted successfully!')
    else:
        messages.error(request, 'You can only delete your own comments!')

    
    return redirect(reverse('lessons_detail', args=[slug]))

def book_a_lesson(request):
    today = datetime.now().date()
    year = today.year
    month = today.month

    # create the calendar for the current month
    cal = calendar.Calendar(firstweekday=0)
    month_days = cal.monthdayscalendar(year, month)

    # get LessonDates for the current month
    lesson_dates = LessonDate.objects.filter(date__year=year, date__month=month)

    context = {
        'year': year,
        'month': month,
        'month_days': month_days,
        'lesson_dates': lesson_dates,
    }

    return render(request, 'bookalesson/book_a_lesson.html', context)



def timeslots_for_date(request, date):
    try:
        day, month = map(int, date.split('-'))
        year = datetime.now().year  
        date_obj = datetime(year, month, day).date()
    except ValueError:
        return HttpResponseBadRequest("Invalid date format. Expected DD-MM.")

    # set the time slots from 8 AM to 6 PM
    start_time = datetime(year, month, day, 8, 0)
    end_time = datetime(year, month, day, 18, 0)
    time_slots = []
    
    current_time = start_time
    while current_time <= end_time:
        time_slots.append(current_time.time()) 
        current_time += timedelta(hours=1)
    
    # get booked slots for the selected date
    booked_slots = LessonDate.objects.filter(date=date_obj).values_list('start_time', 'end_time')
    
    # dont show booked slots from the available time slots
    available_slots = []
    for slot in time_slots:
        # check if itmeslots are within any booked time range
        is_booked = any(start <= slot < end for start, end in booked_slots)
        if not is_booked:
            available_slots.append(slot.strftime("%H:%M"))
    
    context = {
        'date': date_obj,
        'time_slots': available_slots,
    }

    return render(request, 'bookalesson/timeslots.html', context)


    
@login_required
def booking_form(request, date, slot):
    print(f"Received date: {date}, slot: {slot}")

    try:
        # change timeslot to time format
        slot_time = datetime.strptime(slot, '%H:%M').time()
        print(f"Slot time parsed: {slot_time}")
    except ValueError:
        print(f"Invalid time format for slot: {slot}")
        raise Http404("Invalid time format")

    # check if the LessonDate already exists or create a new one
    lesson_date, created = LessonDate.objects.get_or_create(
        date=date,
        start_time=slot_time,
        defaults={
            'end_time': slot_time, 
            'lesson': Lesson.objects.first(), 
            'slug': f"{date}-{slot.replace(':', '-')}",
            'user': request.user  
        }
    )
    if created:
        # create a unique slug if the LessonDate is newly created
        lesson_date.slug = f"{date}-{slot.replace(':', '-')}"
        while LessonDate.objects.filter(slug=lesson_date.slug).exists():
            lesson_date.slug = f"{date}-{slot.replace(':', '-')}-{LessonDate.objects.count()}"
        lesson_date.save()
        print(f"LessonDate created with slug: {lesson_date.slug}")

    if request.method == 'POST':
        user = request.user
        if not user.is_authenticated:
            messages.error(request, "You need to log in to make a booking.")
            return redirect('login')

        # get selected lesson and instructor from POST data
        lesson_id = request.POST.get('lesson_type')
        instructor_id = request.POST.get('instructor')

        try:
            lesson = Lesson.objects.get(pk=lesson_id)
            instructor = Instructor.objects.get(pk=instructor_id)
        except (Lesson.DoesNotExist, Instructor.DoesNotExist):
            messages.error(request, "Selected lesson or instructor does not exist.")
            return redirect('book_a_lesson')

        # check if the slot is already booked
        existing_booking = Booking.objects.filter(lesson_date=lesson_date).exists()
        if existing_booking:
            messages.error(request, "This time slot is already booked.")
            return redirect('book_a_lesson')

        # create a new booking
        booking = Booking(
            user=user,
            lesson_date=lesson_date,
            lesson_type=lesson,
            instructor=instructor,
        )
        booking.save()

        # generate a detailed success message
        success_message = (
            f"Your booking for the lesson '{lesson.title}' with instructor '{instructor.name}' "
            f"on {date} from {slot_time} to {lesson_date.end_time} has been received and is pending approval by the instructor."
        )
        messages.success(request, success_message)
        return redirect('book_a_lesson')

    # get all lessons and instructors for the form
    lessons = Lesson.objects.all()
    instructors = Instructor.objects.all()

    return render(request, 'bookalesson/booking_form.html', {
        'lesson_date': lesson_date,
        'lessons': lessons,
        'instructors': instructors
    })