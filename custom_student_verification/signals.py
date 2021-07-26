"""
Signal handler for setting manual student verification data.
"""

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from custom_student_verification.compat import (
    get_course_enrollment_model,
    get_course_mode_model,
    get_manual_verification_model,
)
from custom_student_verification.models import StudentVerificationRequest
from custom_student_verification.utils import send_verification_approved_email, send_verification_rejected_email


@receiver(post_save, sender=StudentVerificationRequest)
def on_student_verification_request_saved(sender, instance, **kwargs):  # pylint: disable=unused-argument
    """
    Triggered when StudentVerificationRequest is saved.

    If status is accepted calls approve_user() to create ManualVerification if not exists
    """
    if instance.status == 'ACCEPTED':
        approve_user(instance.user, instance.reason)
    elif instance.status == 'REJECTED':
        reject_user(instance.user, instance.reason)


def approve_user(user, reason):
    """
    Create ManualVerification object for the user if it doesn't already exist.

    We use a separate function here so we can mock it during tests
    """
    ManualVerification = get_manual_verification_model()
    if not ManualVerification.objects.filter(user=user, status='approved').exists():
        ManualVerification.objects.create(
            user=user,
            status='approved',
            reason=reason if reason else 'N/A',
            name=user.profile.name
        )
        # send an email to the user about verification approval.
        send_verification_approved_email(user, reason)


def reject_user(user, reason):
    """
    Handler for ID verifiation rejection.

    Deletes the approved ManualVerification records for user and send an
    email informing user of the verification request rejection.
    """
    ManualVerification = get_manual_verification_model()
    # delete all approved ManualVerification records for user.
    ManualVerification.objects.filter(user=user, status='approved').delete()
    # send an email to the user about verification rejection.
    send_verification_rejected_email(user, reason)


@receiver(post_save, sender=get_course_enrollment_model())
def auto_verify_paid_students(sender, instance, created, **kwargs):  # pylint: disable=unused-argument
    """
    Veriy the learner who paid for the course.

    Signal helps to auto-verify student who are paying for the course.
    This signal will only take effect when the switch is enabled.
    """
    course_mode = get_course_mode_model()
    if settings.FEATURES.get('ENABLE_PAID_COURSE_AUTO_VERIFY'):
        if instance.mode == course_mode.VERIFIED:
            approve_user(instance.user, 'auto-verification')
