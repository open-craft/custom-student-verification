# pylint: disable=import-outside-toplevel
"""
Proxies, and compatibility code for edx-platform features.

This module moderates access to all edx-platform features allowing for
cross-version compatibility code.

It is also simplifies running tests outside of edx-platform's environment
by stubbing these functions in unit tests.
"""


def get_manual_verification_model():
    """
    Get ManualVerification model.
    """
    try:
        from lms.djangoapps.verify_student.models import ManualVerification
        return ManualVerification
    except ImportError:
        return object


def get_language_key():
    """
    Get the LANGUAGE_KEY from openedx.
    """
    try:
        from openedx.core.djangoapps.lang_pref import LANGUAGE_KEY
        return LANGUAGE_KEY
    except ImportError:
        return 'perf-lang'


def get_user_preference_model():
    """
    Get the UserPreference model.
    """
    try:
        from openedx.core.djangoapps.user_api.models import UserPreference
        return UserPreference
    except ImportError:
        return object


def get_base_template_context(site):
    """
    Compatibility function for the get_base_template_context.

    Returns the context if get_base_template_context is imported else
    returns empty dictionary.
    """
    try:
        from openedx.core.djangoapps.ace_common.template_context import get_base_template_context as get_context
        return get_context(site)
    except ImportError:
        return {}


def get_base_message_type():
    """
    Get BaseMessageType class.
    """
    try:
        from openedx.core.djangoapps.ace_common.message import BaseMessageType
        return BaseMessageType
    except ImportError:
        from edx_ace.message import MessageType
        return MessageType


def get_course_enrollment_model():
    """
    Get CourseEnrollment model.
    """
    try:
        from common.djangoapps.student.models import CourseEnrollment
        return CourseEnrollment
    except ImportError:
        return object


def get_course_mode_model():
    """
    Get CourseMode model.
    """
    try:
        from common.djangoapps.course_modes.models import CourseMode
        return CourseMode
    except ImportError:
        return object
