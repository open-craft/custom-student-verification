"""
Tests for signal receivers of custom_verification_app.
"""
from unittest.mock import MagicMock, Mock, patch

from django.contrib.auth.models import User
from django.contrib.admin.sites import AdminSite
from django.db import IntegrityError
from django.test import TestCase
from custom_student_verification.admin import StudentVerificationRequestAdmin

from custom_student_verification.models import StudentVerificationRequest


class StudentVerificationRequestAdminTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username="testuser", email="test@example.clm")
        self.user.profile = MagicMock()
        self.user.profile.name.return_value = "Test User"
        return super().setUp()

    @patch('custom_student_verification.signals.reject_user')
    @patch('custom_student_verification.signals.approve_user')
    def test_update_fields_in_queryset_successfully(self, mock_reject_method, mock_approve_method):
        expected_successfully_updates = 3
        expected_failed_updates = 0

        StudentVerificationRequest.objects.create(
            user=self.user,
            status="PENDING",
        )
        StudentVerificationRequest.objects.create(
            user=self.user,
            status="PENDING"
        )
        StudentVerificationRequest.objects.create(
            user=self.user,
            status='REJECTED'
        )

        admin_site = StudentVerificationRequestAdmin(admin_site=AdminSite, model=StudentVerificationRequest)
        successfully_updated, failed_to_update = admin_site.update_fields_for_queryset(
            StudentVerificationRequest.objects.all(), 'status', 'ACCEPTED',
        )

        self.assertEqual(successfully_updated, expected_successfully_updates)
        self.assertEqual(failed_to_update, expected_failed_updates)

    def test_update_fields_in_queryset_and_some_updates_fail(self):
        expected_successfully_updates = 2
        expected_failed_updates = 1

        queryset = MagicMock()
        item_success_1 = Mock()
        item_to_fail = Mock()
        item_success_2 = Mock()
        item_to_fail.save.side_effect = IntegrityError
        queryset_items = [item_success_1, item_to_fail, item_success_2]
        queryset.__iter__.return_value = iter(queryset_items)
        admin_site = StudentVerificationRequestAdmin(admin_site=AdminSite, model=StudentVerificationRequest)

        successfully_updated, failed_to_update = admin_site.update_fields_for_queryset(
            queryset, 'status', 'ACCEPTED',
        )

        # assert results of updating the status of items to accepted
        self.assertEqual(successfully_updated, expected_successfully_updates)
        self.assertEqual(failed_to_update, expected_failed_updates)

        # assert save method is called on each queryset item
        for qs_item in queryset_items:
            qs_item.save.assert_called_once()

    @patch('custom_student_verification.signals.reject_user')
    @patch('custom_student_verification.signals.approve_user')
    def test_bulk_approve_multiple_verification_requests(self, mock_reject_method, mock_approve_method):
        expected_accepted_verification_requests = 4
        expected_rejected_verification_requests = 0
        expected_pending_verification_requests = 0

        StudentVerificationRequest.objects.create(
            user=self.user,
            status="PENDING",
        )
        StudentVerificationRequest.objects.create(
            user=self.user,
            status="PENDING"
        )
        StudentVerificationRequest.objects.create(
            user=self.user,
            status="REJECTED",
        )
        StudentVerificationRequest.objects.create(
            user=self.user,
            status="ACCEPTED"
        )
        request = MagicMock()

        admin_site = StudentVerificationRequestAdmin(admin_site=AdminSite, model=StudentVerificationRequest)
        admin_site.bulk_approve(request, StudentVerificationRequest.objects.all())

        accepted_requests = StudentVerificationRequest.objects.filter(status='ACCEPTED').count()
        rejected_requests = StudentVerificationRequest.objects.filter(status='REJECTED').count()
        pending_requests = StudentVerificationRequest.objects.filter(status='PENDING').count()

        self.assertEqual(accepted_requests, expected_accepted_verification_requests)
        self.assertEqual(rejected_requests, expected_rejected_verification_requests)
        self.assertEqual(pending_requests, expected_pending_verification_requests)
