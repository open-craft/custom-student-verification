"""
Tests for implemented django admin features
"""
from unittest.mock import MagicMock, Mock, patch

import ddt
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase

from custom_student_verification.admin import StudentVerificationRequestAdmin
from custom_student_verification.models import StudentVerificationRequest


def get_item_that_throws_integrity_error_on_save():
    """
    Returns a mocked element that on save method call will throw an IntegrityError exception
    """
    mocked_item = Mock()
    mocked_item.save.side_effect = IntegrityError
    return mocked_item


@ddt.ddt
class StudentVerificationRequestAdminTest(TestCase):
    """
    Tests for StudentVerificationRequestAdmin features
    """
    def setUp(self) -> None:
        self.user = User.objects.create(username="testuser", email="test@example.clm")
        self.user.profile = MagicMock()
        self.user.profile.name.return_value = "Test User"
        return super().setUp()

    @ddt.data(
        ([Mock(), get_item_that_throws_integrity_error_on_save(), Mock()], 2, 1),
        ([Mock(), Mock(), Mock()], 3, 0)
    )
    @ddt.unpack
    def test_update_fields_in_queryset_and_some_updates_fail(
            self, queryset_items, expected_successfully_updates, expected_failed_updates
    ):
        """
        Test that save method is called on each element of queryset, and that counters for successful updates
        and failed ones, have the right results
        """
        queryset = MagicMock()
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
    def test_bulk_approve_multiple_verification_requests(
            self, mock_reject_method, mock_approve_method
    ):  # pylint: disable=unused-argument
        """
        Test bulk_approve set correctly the status of multiple verification requests to ACCEPTED
        """
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
