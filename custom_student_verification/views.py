"""
custom_student_verification App certificate search API view.
"""
from __future__ import absolute_import, unicode_literals

from django.contrib.auth.mixins import LoginRequiredMixin
from django.middleware.csrf import get_token
from django.shortcuts import redirect, render
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.generic import TemplateView
from xblockutils.resources import ResourceLoader

from .forms import UploadIDForm
from .models import StudentVerificationRequest

loader = ResourceLoader(__name__)


class CustomStudentVerificationView(LoginRequiredMixin, TemplateView):
    """
    View to display status for and receive applications for Student Verification Requests.
    """

    @staticmethod
    def last_attempt_status(user):
        """
        Return the status and reason for the student's last verification attempt.
        """
        try:
            last_attempt = StudentVerificationRequest.objects.filter(user=user).order_by('-time_created')[0]
            return last_attempt.status, last_attempt.reason
        except IndexError:
            return None, None

    @xframe_options_sameorigin
    def get(self, request, *args, **kwargs):
        """
        Fetch last application status and render the template.
        """
        form = UploadIDForm()
        last_attempt_status, reason = CustomStudentVerificationView.last_attempt_status(request.user)
        csrf_token = get_token(request)
        return render(request, 'custom_student_verification.html', {
            'form': form,
            'last_attempt_status': last_attempt_status,
            'reason': reason,
            'csrf_token': csrf_token,
        })

    def post(self, request, *args, **kwargs):
        """
        Receive and save student verification request if it is valid.
        """
        last_attempt_status, _reason = CustomStudentVerificationView.last_attempt_status(request.user)
        instance = StudentVerificationRequest(user=request.user)
        form = UploadIDForm(request.POST, request.FILES, instance=instance)

        if form.is_valid() and last_attempt_status not in ['PENDING', 'ACCEPTED']:
            form.save()

        return redirect('custom_student_verification_app:custom-student-verification')
