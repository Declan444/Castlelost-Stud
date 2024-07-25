# Generated by Django 4.2.14 on 2024-07-25 20:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("bookalesson", "0005_bookingdate"),
    ]

    operations = [
        migrations.CreateModel(
            name="CommentOnLesson",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.TextField()),
                ("approved", models.BooleanField(default=False)),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "lesson_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bookalesson.lessontype",
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="commentonlesson",
            constraint=models.UniqueConstraint(
                fields=("author", "lesson_type"), name="unique_user_lesson_comment"
            ),
        ),
    ]
