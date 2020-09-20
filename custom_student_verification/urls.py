"""
URL configuration for custom_student_verification app.
"""
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from .views import CustomStudentVerificationView

urlpatterns = (
    url(r'^custom-student-verification$', CustomStudentVerificationView.as_view(), name="custom-student-verification"),
)
