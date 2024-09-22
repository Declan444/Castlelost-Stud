from django.test import TestCase
from .models import Instructor


# Instructor Model Tests
# -----------------------------------------------
class InstructorModelTest(TestCase):
    
    def setUp(self):
        """
        Create an instructor instance for testing.
        """
        self.instructor = Instructor.objects.create(
            name="Declan Lenahan",
            bio="An experienced instructor.",
            slug="declan-lenahan"
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
            slug="declan-lenahan"  # This should raise an IntegrityError
        )
        with self.assertRaises(Exception):  # Catch the exception when saving
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