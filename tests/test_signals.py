"""
Tests for signal receivers of custom_verification_app.
"""
from unittest.mock import MagicMock, patch

from django.contrib.auth.models import User
from django.test import TestCase

from custom_student_verification.models import StudentVerificationRequest


class VerificationSignalTestCase(TestCase):
    """
    Tests for signal receivers of custom_verification_app.
    """

    def setUp(self) -> None:
        self.user = User.objects.create(username="testuser", email="test@example.clm")
        self.user.profile = MagicMock()
        self.user.profile.name.return_value = "Test User"
        self.verification_request = StudentVerificationRequest.objects.create(
            user=self.user,
            status="PENDING"
        )
        return super().setUp()

    @patch('custom_student_verification.signals.get_manual_verification_model')
    @patch('custom_student_verification.signals.send_verification_rejected_email')
    def test_rejection_email_is_sent(self, mock_email, mock_model_method):
        """
        Tests that the email is sent when verification is rejected.
        """
        mock_manual_verification_model = MagicMock()
        mock_model_method.return_value = mock_manual_verification_model

        self.verification_request.status = "REJECTED"
        self.verification_request.reason = "Reason for rejection"
        self.verification_request.save()
        mock_email.assert_called_with(self.user, "Reason for rejection")

    @patch('custom_student_verification.signals.get_manual_verification_model')
    @patch('custom_student_verification.signals.send_verification_approved_email')
    def test_approval_email_is_sent(self, mock_email, mock_model_method):
        """
        Test that the email is sent when verification request is approved.
        """
        mock_manual_verification_model = MagicMock()
        mock_model_method.return_value = mock_manual_verification_model
        mock_manual_verification_model.objects.filter().exists.return_value = False

        self.verification_request.status = "ACCEPTED"
        self.verification_request.reason = "Reason for accepting"
        self.verification_request.save()
        mock_email.assert_called_with(self.user, "Reason for accepting")
