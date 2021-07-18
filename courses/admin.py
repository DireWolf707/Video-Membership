from django.contrib import admin
from .models import Course, Lesson


class LessonStackedInline(admin.TabularInline):
    model = Lesson
    prepopulated_fields = {"slug": ("title",)}
    extra = 0


class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonStackedInline]
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Course, CourseAdmin)
