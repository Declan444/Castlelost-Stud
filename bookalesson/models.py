from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


def get_default_lesson_date():
    return timezone.now().date()


# Create your models here.
class Instructor(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField()
    slug = models.SlugField(max_length=200, unique=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Instructor: {self.name}"


class Lesson(models.Model):
    LESSON_CHOICES = (
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    lesson_choices = models.CharField(max_length=20, choices=LESSON_CHOICES)
    instructor = models.ForeignKey(
        Instructor, on_delete=models.CASCADE, related_name="lesson_types"
    )
    content = models.TextField()
    excerpt = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title}"


class LessonDate(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    slug = models.SlugField(unique=True, blank=True)
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="lesson_dates"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="booked_lesson_dates"
    )

    def __str__(self):
        return (
            f"{self.lesson.title} on {self.date} from {self.start_time}"
            f" to {self.end_time}"
        )


class Booking(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending Approval"),
        ("approved", "Approved"),
        ("cancelled", "Cancelled"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson_date = models.ForeignKey(LessonDate, on_delete=models.CASCADE)
    lesson_type = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending"
    )
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"Booking by {self.user.username} for {self.lesson_type}"
            f" with {self.instructor.name}"
        )


class CommentOnLesson(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson_type = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="comments"
    )
    lesson_date = models.ForeignKey(
        LessonDate,
        on_delete=models.CASCADE,
        related_name="comments",
        null=True,
        blank=True,
    )
    text = models.TextField()

    approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["author", "lesson_type", "lesson_date"],
                name="unique_user_lesson_date_comment",
            )
        ]

    def __str__(self):
        return (
            f"Comment by {self.author} on {self.lesson_type.title}"
            f" on {self.lesson_date}"
        )
