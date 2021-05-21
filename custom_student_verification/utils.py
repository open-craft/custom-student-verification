"""
Utility functions for custom_student_verfication app.
"""
import logging

from django.conf import settings
from django.contrib.sites.models import Site
from edx_ace import ace
from edx_ace.recipient import Recipient

from custom_student_verification.compat import get_base_template_context, get_language_key, get_user_preference_model
from custom_student_verification.message_types import VerificationApproved, VerificationRejected

LANGUAGE_KEY = get_language_key()


log = logging.getLogger(__name__)
UserPeference = get_user_preference_model()


def _send_verification_email(message_type, context):
    """
    Send and email the user through edx_ace using message_type.
    """
    site = Site.objects.get_current()
    message_context = get_base_template_context(site)
    message_context.update(context)
    user = context['user']
    try:
        msg = message_type(context=message_context).personalize(
            recipient=Recipient(user.id, user.email),
            language=UserPeference.get_value(user, LANGUAGE_KEY, default=settings.LANGUAGE_CODE),
            user_context={'full_name': user.profile.name}
        )
        ace.send(msg)
        log.info('%s message sent to user: %r', message_type.__name__, user.username)
        return True
    except Exception:  # pylint: disable=broad-except
        log.exception('Could not send message of type %s to user %s', message_type.__name__, user.username)
        return False


def send_verification_rejected_email(user, reason):
    """
    Send email to learner about ID verification rejection.
    """
    email_context = {
        'user': user,
        'reason': reason
    }
    return _send_verification_email(VerificationRejected, email_context)


def send_verification_approved_email(user, reason):
    """
    Send email to learner about ID verification approval.
    """
    email_context = {
        'user': user,
        'reason': reason
    }
    return _send_verification_email(VerificationApproved, email_context)
