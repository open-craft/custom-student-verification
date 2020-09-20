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
