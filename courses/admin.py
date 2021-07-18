from django.contrib import admin
from .models import Course, Lesson


class LessonStackedInline(admin.StackedInline):
    model = Lesson


class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonStackedInline]


admin.site.register(Course, CourseAdmin)
