from django.shortcuts import render, get_object_or_404, redirect
from .models import CommentOnLesson, LessonDate, Booking
from django import forms
from django.contrib import messages


class CommentForm(forms.ModelForm):
    lesson_date = forms.ModelChoiceField(
        # Placeholder; will be set dynamically in the view
        queryset=LessonDate.objects.none(),  
        required=True,
        empty_label="Select a lesson date",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = CommentOnLesson
        #fields to be included in the form
        fields = ['text', 'lesson_date']  

    def __init__(self, *args, **kwargs):
        
        lesson_dates = kwargs.pop('lesson_dates', LessonDate.objects.none())
        super().__init__(*args, **kwargs)
        self.fields['lesson_date'].queryset = lesson_dates

def booking_form(request, date, slot):
    
    lesson_date = get_object_or_404(LessonDate, date=date, start_time=slot)

    if request.method == 'POST':
        
        user = request.user  
        if not user.is_authenticated:
            messages.error(request, "You need to log in to make a booking.")
            return redirect('login')  

        # check if the slot is already booked
        existing_booking = Booking.objects.filter(lesson_date=lesson_date).exists()
        if existing_booking:
            messages.error(request, "This time slot is already booked.")
            return redirect('book_a_lesson')  

        # Create a new booking
        booking = Booking(
            user=user,
            lesson_date=lesson_date,
            lesson_type=lesson_date.lesson,
            instructor=lesson_date.lesson.instructor,  
        )
        booking.save()

        # Inform the user and redirect
        messages.success(request, "Your booking is pending approval.")
        return redirect('book_a_lesson')  

    return render(request, 'booking_form.html', {'lesson_date': lesson_date})

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['lesson_date', 'lesson_type', 'instructor']
        widgets = {
            'lesson_date': forms.HiddenInput(),
            'lesson_type': forms.HiddenInput(),
            'instructor': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        
        super(BookingForm, self).__init__(*args, **kwargs)
        self.fields['lesson_date'].widget.attrs.update({'class': 'form-control'})
        self.fields['lesson_type'].widget.attrs.update({'class': 'form-control'})
        self.fields['instructor'].widget.attrs.update({'class': 'form-control'})