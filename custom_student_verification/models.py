"""
Model for Student Verification Requests.

This model stores a user's verification request, status and reason
"""
from django.contrib.auth.models import User
from django.db import models
from django.utils.html import mark_safe

STATUS_CHOICES = [(u'PENDING', 'PENDING'), (u'ACCEPTED', 'ACCEPTED'), (u'REJECTED', 'REJECTED')]


class StudentVerificationRequest(models.Model):
    """
    Model to track identity verification requests through a Photo ID.

    .. pii: Stores photo id for the user.
    .. pii_types: image
    .. pii_retirement: retained
    """

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    id_photo = models.ImageField(upload_to=u'student_verification_requests')
    status = models.CharField(choices=STATUS_CHOICES, default='PENDING', max_length=8)
    reason = models.CharField(blank=True, null=True, default=None, max_length=256)
    time_created = models.DateTimeField(auto_now_add=True)
    time_modified = models.DateTimeField(auto_now=True)

    def photo_id_tag(self):
        """
        Return <img> tag with SRC set as the photo ID provided by the student.
        """
        return mark_safe('<img src="%s" style="max-height:15rem;" />' % self.id_photo.url)
