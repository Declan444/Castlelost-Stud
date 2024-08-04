from .models import CommentOnLesson, LessonDate
from django import forms


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
        # Extract 'lesson_dates' from kwargs if provided; default to an empty queryset if not
        lesson_dates = kwargs.pop('lesson_dates', LessonDate.objects.none())
        # Initialize the parent class (ModelForm) with the provided arguments
        super().__init__(*args, **kwargs)
        # Update the queryset for the 'lesson_date' field with the provided lesson dates
        self.fields['lesson_date'].queryset = lesson_dates
