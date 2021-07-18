from django.shortcuts import render, get_object_or_404
from django.contrib.auth.views import redirect_to_login
from django.views import View
from django.views.generic import ListView
from .models import Course, Lesson
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import AccessMixin


class CourseListView(ListView):
    model = Course
    context_object_name = 'courses'
    template_name = 'course_list.html'


class CourseDetailView(View):
    def get(self, request, *args, **kwargs):
        course = get_object_or_404(Course, slug=self.kwargs['course_slug'])
        lessons = course.lessons.all().order_by('order')
        return render(request, 'course_detail.html', {'course': course, 'lessons': lessons})


class LessonDetailView(AccessMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        lesson = get_object_or_404(Lesson,
                                   slug=self.kwargs['lesson_slug'],
                                   course=self.course)
        return render(request, 'lesson_detail.html', {'lesson': lesson})

    def check_membership(self):
        self.course = get_object_or_404(Course,
                                        slug=self.kwargs['course_slug']
                                        )
        return self.request.user.membership.membership_type in self.course.memberships_required.all()

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())
        user_test_result = self.check_membership()
        if not user_test_result:
            return HttpResponse("Upgrade membership")
        return super().dispatch(request, *args, **kwargs)
