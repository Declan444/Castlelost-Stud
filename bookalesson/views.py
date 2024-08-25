
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import Http404, JsonResponse
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
    
    # how all the lesson dates for the specific user if authenticated
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

    correct_lesson_date = comment.lesson_date
    if correct_lesson_date:
        correct_lesson_date_str = f"{correct_lesson_date.date} from {correct_lesson_date.start_time} to {correct_lesson_date.end_time}"
    else:
        correct_lesson_date_str = "Not available"

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST, instance=comment, lesson_dates=lesson_dates)
        if comment_form.is_valid() and comment.author == request.user:
            try:
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.approved = False
                comment.save()
                messages.success(request, 'Comment updated successfully!')
                return redirect(reverse('lessons_detail', args=[slug]))
            except IntegrityError:
                messages.error(
                    request,
                    f'You have selected an incorrect lesson date. The correct lesson date is: {correct_lesson_date_str}. '
                    'Please ensure your lesson dates are correct and try again.'
                )
        else:
            messages.error(request, 'Error updating comment! Please ensure all fields are correctly filled.')
    else:
        comment_form = CommentForm(instance=comment, lesson_dates=lesson_dates)

    context = {
        'comment_form': comment_form,
        'lesson': post,
        'comment': comment,
        'selected_lesson_date_id': comment.lesson_date.id if comment.lesson_date else None,
        'correct_lesson_date_str': correct_lesson_date_str,
    }
    return redirect(reverse('lessons_detail', args=[slug]))

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
    today_date_str = today.strftime('%d-%m-%Y')

    year = request.GET.get('year', today.year)
    month = request.GET.get('month', today.month)

    try:
        year = int(year)
        month = int(month)
    except ValueError:
        return HttpResponseBadRequest("Invalid year or month.")

    if month < 1 or month > 12:
        return HttpResponseBadRequest("Month must be between 1 and 12.")

    prev_year = year - 1 if month == 1 else year
    prev_month = 12 if month == 1 else month - 1
    next_year = year + 1 if month == 12 else year
    next_month = 1 if month == 12 else month + 1

    cal = calendar.Calendar(firstweekday=0)
    month_days = cal.monthdayscalendar(year, month)

    # Change dates_status to a dictionary
    dates_status_dict = {}
    for week in month_days:
        for day in week:
            if day:
                day_formatted = f"{day:02d}"
                month_formatted = f"{month:02d}"
                year_formatted = f"{year:04d}"
                day_date_str = f"{day_formatted}-{month_formatted}-{year_formatted}"
                day_date = datetime.strptime(day_date_str, '%d-%m-%Y').date()
                is_past = day_date < today
                dates_status_dict[day_date_str] = is_past

    context = {
        'year': year,
        'month': month,
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
        'month_days': month_days,
        'today_date_str': today_date_str,
        'dates_status': dates_status_dict,  # Pass as a dictionary
    }

    return render(request, 'bookalesson/book_a_lesson.html', context)





@login_required
def timeslots_for_date(request, date):
    try:
        # Expecting date in dd-mm-yyyy format
        date_obj = datetime.strptime(date, '%d-%m-%Y').date()
        year = date_obj.year
        month = date_obj.month
        day = date_obj.day
    except ValueError:
        return HttpResponseBadRequest("Invalid date format. Expected dd-mm-yyyy.")

    # Set the time slots from 8 AM to 6 PM
    start_time = datetime(year, month, day, 8, 0)
    end_time = datetime(year, month, day, 18, 0)
    time_slots = []

    current_time = start_time
    while current_time <= end_time:
        time_slots.append(current_time.time())
        current_time += timedelta(hours=1)

    # Get booked slots for the selected date
    booked_slots = LessonDate.objects.filter(date=date_obj).values_list('start_time', 'end_time')

    # Get the current time
    now = datetime.now()
    current_time_today = now.time()
    
    # Determine if the date is today
    is_today = (date_obj == now.date())

    # Create a list of slots with their booking status
    slots_with_status = []
    for slot in time_slots:
        # Determine if slot is booked
        is_booked = any(start <= slot < end for start, end in booked_slots)
        
        # Make past times inactive if it's today
        if is_today and slot < current_time_today:
            is_booked = True  # Consider past times as booked

        slots_with_status.append({
            'time': slot.strftime("%H:%M"),
            'is_booked': is_booked
        })

    context = {
        'date': date_obj,
        'slots_with_status': slots_with_status,
    }

    return render(request, 'bookalesson/timeslots.html', context)

    
@login_required
def booking_form(request, date, slot):
    print(f"Received date: {date}, slot: {slot}")
    try:
        
        # Convert slot to time format
        slot_time = datetime.strptime(slot, '%H:%M').time()
        # Calculate end time as one hour later
        end_time = (datetime.combine(datetime.today(), slot_time) + timedelta(hours=1)).time()
        print(f"Parsed slot time: {slot_time}, End time: {end_time}")
    except ValueError:
        raise Http404("Invalid time format")
    
        

    # Retrieve or create LessonDate instance
    lesson_date = LessonDate.objects.filter(date=date, start_time=slot_time).first()
    print(f"Retrieved lesson_date: {lesson_date}")

    if request.method == 'POST':
        user = request.user
        if not user.is_authenticated:
            messages.error(request, "You need to log in to make a booking.")
            return redirect('login')

        # Get selected lesson and instructor from POST data
        lesson_id = request.POST.get('lesson_type')
        instructor_id = request.POST.get('instructor')

        print(f"Selected lesson_id: {lesson_id}, instructor_id: {instructor_id}")

        try:
            lesson = Lesson.objects.get(pk=lesson_id)
            instructor = Instructor.objects.get(pk=instructor_id)
            print(f"Retrieved lesson: {lesson.title}, instructor: {instructor.name}")
        except (Lesson.DoesNotExist, Instructor.DoesNotExist):
            messages.error(request, "Selected lesson or instructor does not exist.")
            return redirect('book_a_lesson')

        # If the LessonDate does not exist, create it
        if not lesson_date:
            lesson_date = LessonDate(
                date=date,
                start_time=slot_time,
                end_time=end_time,
                lesson=lesson,
                slug=f"{date}-{slot.replace(':', '-')}",
                user=user
            )
            # Create a unique slug
            while LessonDate.objects.filter(slug=lesson_date.slug).exists():
                lesson_date.slug = f"{date}-{slot.replace(':', '-')}-{LessonDate.objects.count()}"
            lesson_date.save()
            print(f"Created new lesson_date with slug: {lesson_date.slug}")

        # Check if the slot is already booked
        existing_booking = Booking.objects.filter(lesson_date=lesson_date).exists()
        print(f"Existing booking for this lesson_date: {existing_booking}")
        if existing_booking:
            messages.error(request, "This time slot is already booked.")
            return redirect('book_a_lesson')

        # Create a new booking
        booking = Booking(
            user=user,
            lesson_date=lesson_date,
            lesson_type=lesson,
            instructor=instructor,
        )
        booking.save()
        print(f"Created booking for user: {user.username}, lesson: {lesson.title}, instructor: {instructor.name}")

        # Generate a detailed success message
        success_message = (
            f"Your booking for the lesson '{lesson.title}' with instructor '{instructor.name}' "
            f"on {date} from {slot_time} to {end_time} has been received and is pending approval by the instructor."
        )
        messages.success(request, success_message)
        return redirect('book_a_lesson')

    # Get all lessons and instructors for the form
    lessons = Lesson.objects.all()
    instructors = Instructor.objects.all()
    

    context = {
        'lesson_date': lesson_date,
        'lessons': lessons,
        'instructors': instructors
    }

    return render(request, 'bookalesson/booking_form.html', context)

def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
       
        
        # Respond with a JSON response to indicate success
        return JsonResponse({'success': True})

    return render(request, 'bookalesson/contact_us.html')
        
       
       
