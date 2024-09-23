from django.test import TestCase
from .models import Instructor, Lesson


# Instructor Model Test
# -----------------------------------------------
class InstructorModelTest(TestCase):

    def setUp(self):
        """
        Create an instructor instance for testing.
        """
        self.instructor = Instructor.objects.create(
            name="Declan Lenahan",
            bio="An experienced instructor.",
            slug="declan-lenahan",
        )

    def test_instructor_str(self):
        """
        Test the string representation of the Instructor model.
        """
        self.assertEqual(str(self.instructor), "Instructor: Declan Lenahan")

    def test_instructor_slug_unique(self):
        """
        Test that the slug field is unique.
        """
        instructor2 = Instructor(
            name="Jane Smith",
            bio="Another experienced instructor.",
            slug="declan-lenahan",  
        )
        with self.assertRaises(Exception):  
            instructor2.save()

    def test_instructor_bio_max_length(self):
        """
        Test that the bio field accepts long text.
        """
        # Create a long string
        long_bio = "a" * 1000
        self.instructor.bio = long_bio
        self.instructor.save()
        self.assertEqual(self.instructor.bio, long_bio)


# Lesson Model Test
# ------------------------------------------------
class LessonModelTest(TestCase):

    def setUp(self):
        """
        Create an Instructor instance for the ForeignKey
        """
        self.instructor = Instructor.objects.create(
            name="Jane Smith", bio="Expert in showjumping.", slug="jane-smith"
        )

        """
        Create a Lesson instance
        """
        self.lesson = Lesson.objects.create(
            title="Pole Work",
            slug="pole-work",
            lesson_choices="beginner",
            instructor=self.instructor,
            content="This lesson covers the basics of Showjumping.",
            excerpt="Beginners Lesson in Showjumping.",
        )
        """
        Test case for lesson creation
        """

    def test_lesson_creation(self):
        # Check if the lesson was created correctly
        self.assertIsInstance(self.lesson, Lesson)
        self.assertEqual(self.lesson.title, "Pole Work")
        self.assertEqual(self.lesson.lesson_choices, "beginner")
        self.assertEqual(self.lesson.instructor, self.instructor)
        self.assertEqual(
            self.lesson.content,
            "This lesson covers the basics of Showjumping.",
        )
        self.assertEqual(
            self.lesson.excerpt, "Beginners Lesson in Showjumping."
        )

    def test_str_method(self):
        self.assertEqual(str(self.lesson), "Pole Work")
