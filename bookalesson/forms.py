from django.shortcuts import render, get_object_or_404, redirect
from .models import CommentOnLesson, LessonDate, Booking
from django import forms
from django.contrib import messages

# Comment Form
#------------------------------------------------
class CommentForm(forms.ModelForm):
    lesson_date = forms.ModelChoiceField(
        # Placeholder; will be set dynamically in the view
        queryset=LessonDate.objects.none(),
        required=True,
        empty_label="Select a lesson date",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = CommentOnLesson
        # fields to be included in the form
        fields = ["text", "lesson_date"]

    def __init__(self, *args, **kwargs):

        lesson_dates = kwargs.pop("lesson_dates", LessonDate.objects.none())
        super().__init__(*args, **kwargs)
        self.fields["lesson_date"].queryset = lesson_dates

# Booking Form Class
#------------------------------------------------
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["lesson_date", "lesson_type", "instructor"]
        widgets = {
            "lesson_date": forms.HiddenInput(),
            "lesson_type": forms.HiddenInput(),
            "instructor": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):

        super(BookingForm, self).__init__(*args, **kwargs)
        self.fields["lesson_date"].widget.attrs.update(
            {"class": "form-control"}
        )
        self.fields["lesson_type"].widget.attrs.update(
            {"class": "form-control"}
        )
        self.fields["instructor"].widget.attrs.update(
            {"class": "form-control"}
        )
