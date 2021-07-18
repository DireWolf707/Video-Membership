from django.db import models
from memberships.models import Membership


class Course(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=60)
    description = models.TextField()
    memberships_required = models.ManyToManyField(Membership)

    def __str__(self) -> str:
        return self.title


class Lesson(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=60)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()
    video_url = models.URLField()
    thumbnail = models.ImageField()

    def __str__(self) -> str:
        return self.title
