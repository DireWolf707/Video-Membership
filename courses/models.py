from django.db import models
from memberships.models import Membership
from sort_order_field import SortOrderField
from django.urls import reverse


class Course(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=60, unique=True)
    description = models.TextField()
    memberships_required = models.ManyToManyField(Membership)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("courses:course_detail", kwargs={"course_slug": self.slug})


def get_upload_to(instance, filename):
    return f'thumbnails/{instance.course}/{instance.title}/{filename}'


class Lesson(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=60)
    course = models.ForeignKey(Course,
                               on_delete=models.CASCADE, related_name='lessons'
                               )
    order = SortOrderField()
    video_url = models.URLField()
    thumbnail = models.ImageField(upload_to=get_upload_to)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("courses:lesson_detail", kwargs={"course_slug": self.course.slug, "lesson_slug": self.slug})
