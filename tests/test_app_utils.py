"""
Tests for utility functions of custom_student_verfication app.
"""

from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase

from custom_student_verification.message_types import VerificationApproved, VerificationRejected
from custom_student_verification.utils import send_verification_approved_email, send_verification_rejected_email


class VerificationEmailTestCase(TestCase):
    """
    Tests for verification email utility functions.
    """

    def setUp(self) -> None:
        self.user = User.objects.create(username="testuser", email="test@example.com")
        return super().setUp()

    @patch('custom_student_verification.utils._send_verification_email')
    def test_verification_email(self, mock_sender):
        send_verification_rejected_email(self.user, "Reason for rejection")
        context = {
            'user': self.user,
            'reason': "Reason for rejection"
        }
        mock_sender.assert_called_with(VerificationRejected, context)

    @patch('custom_student_verification.utils._send_verification_email')
    def test_verification_rejected_email(self, mock_sender):
        """
        """
        send_verification_approved_email(self.user, "Reason for approval")
        context = {
            'user': self.user,
            'reason': "Reason for approval"
        }
        mock_sender.assert_called_with(VerificationApproved, context)
