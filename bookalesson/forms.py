from .models import CommentOnLesson, LessonDate
from django import forms


class CommentForm(forms.ModelForm):
    lesson_date = forms.ModelChoiceField(
        queryset=LessonDate.objects.none(),  # Placeholder; will be set dynamically in the view
        required=True,
        empty_label="Select a lesson date",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = CommentOnLesson
        fields = ['text', 'lesson_date']  # Include lesson_date in the form fields

    def __init__(self, *args, **kwargs):
        lesson_dates = kwargs.pop('lesson_dates', LessonDate.objects.none())
        super().__init__(*args, **kwargs)
        self.fields['lesson_date'].queryset = lesson_dates

