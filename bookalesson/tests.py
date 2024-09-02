# bookalesson/tests.py
from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch, MagicMock
from bookalesson.models import Lesson, Instructor

class LessonListViewTest(TestCase):

    @patch('bookalesson.views.LessonList.get_queryset')
    def test_lesson_list_view_with_mock(self, mock_get_queryset):
        # Create mock data
        instructor = Instructor(name="John Doe", bio="Expert in Django", slug="john-doe")
        lesson1 = Lesson(title="Introduction to Django", slug="intro-to-django", lesson_choices="beginner", instructor=instructor, content="Comprehensive guide to Django framework.", excerpt="Learn Django basics")
        lesson2 = Lesson(title="Advanced Django", slug="advanced-django", lesson_choices="advanced", instructor=instructor, content="Deep dive into advanced Django topics.", excerpt="Explore advanced Django features")
        
        # Mock the queryset returned by the get_queryset method
        mock_get_queryset.return_value = [lesson1, lesson2]

        # Make a GET request to the LessonList view
        response = self.client.get(reverse('lesson_list'))  # Adjust 'lesson_list' to the actual URL name of your view
        
        # Check if the response is 200 OK
        self.assertEqual(response.status_code, 200)
        
        # Check if the correct template is used
        self.assertTemplateUsed(response, 'bookalesson/lessons.html')
        
        # Check if the context contains the mocked data
        self.assertIn('lessons_list', response.context)
        self.assertEqual(list(response.context['lessons_list']), [lesson1, lesson2])

        # Verify that the mocked method was used
        mock_get_queryset.assert_called_once()
