"""
Signal handler for setting manual student verification data.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver

from custom_student_verification.compat import get_manual_verification_model
from custom_student_verification.models import StudentVerificationRequest


@receiver(post_save, sender=StudentVerificationRequest)
def on_student_verification_request_saved(sender, instance, **kwargs):  # pylint: disable=unused-argument
    """
    Triggered when StudentVerificationRequest is saved.

    If status is accepted calls approve_user() to create ManualVerification if not exists
    """
    if instance.status == 'ACCEPTED':
        approve_user(instance.user, instance.reason)


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
