# pylint: disable=expression-not-assigned
"""
Test CustomStudentVerificationView
"""
from __future__ import absolute_import, unicode_literals

from unittest.mock import patch

import ddt
from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import reverse

from custom_student_verification.models import StudentVerificationRequest
from custom_student_verification.views import CustomStudentVerificationView


@ddt.ddt
class CustomStudentVerificationGetTest(TestCase):
    """
    Test GET requests to CustomStudentVerification view
    """

    def setUp(self):
        super(CustomStudentVerificationGetTest, self).setUp()
        self.student = User.objects.create(
            username='test-user',
            email='test-user@example.com',
        )
        self.view = CustomStudentVerificationView.as_view()
        self.factory = RequestFactory()

    def tearDown(self):
        super(CustomStudentVerificationGetTest, self).tearDown()
        StudentVerificationRequest.objects.filter(user=self.student).all().delete()
        self.student.delete()

    def test_unauthenticated(self):
        request = self.factory.get(
            reverse('custom_student_verification_app:custom-student-verification')
        )
        request.user = AnonymousUser()

        response = self.view(request)
        self.assertEqual(response.status_code, 302)

    def test_basic(self):
        request = self.factory.get(
            reverse('custom_student_verification_app:custom-student-verification')
        )
        request.user = self.student
        response = self.view(request)
        html = response.content.decode('utf-8').strip()

        self.assertEqual(response.status_code, 200)
        self.assertRegex(html, r'<form .*>')
        [self.assertNotIn(keyword, html) for keyword in ['accepted', 'rejected', 'processed']]

    @patch('custom_student_verification.signals.reject_user')
    def test_previously_rejected(self, mock_method):
        StudentVerificationRequest.objects.create(
            user=self.student,
            status='REJECTED'
        )

        mock_method.assert_called_once_with(self.student, None)

        request = self.factory.get(
            reverse('custom_student_verification_app:custom-student-verification')
        )
        request.user = self.student
        response = self.view(request)
        html = response.content.decode('utf-8').strip()

        self.assertEqual(response.status_code, 200)
        self.assertRegex(html, r'<form .*>')
        self.assertIn('rejected', html)
        [self.assertNotIn(keyword, html) for keyword in ['accepted', 'processed']]

    def test_previously_accepted(self):
        with patch('custom_student_verification.signals.approve_user') as mock_approve_user:
            StudentVerificationRequest.objects.create(
                user=self.student,
                status="ACCEPTED"
            )
            mock_approve_user.assert_called_with(self.student, None)

        request = self.factory.get(
            reverse('custom_student_verification_app:custom-student-verification')
        )
        request.user = self.student
        response = self.view(request)
        html = response.content.decode('utf-8').strip()

        self.assertEqual(response.status_code, 200)
        self.assertNotRegex(html, r'<form .*>')
        self.assertIn('accepted', html)
        [self.assertNotIn(keyword, html) for keyword in ['processed', 'rejected']]

    def test_previously_pending(self):
        StudentVerificationRequest.objects.create(
            user=self.student,
            status='PENDING'
        )

        request = self.factory.get(
            reverse('custom_student_verification_app:custom-student-verification')
        )
        request.user = self.student
        response = self.view(request)
        html = response.content.decode('utf-8').strip()

        self.assertEqual(response.status_code, 200)
        self.assertNotRegex(html, r'<form .*>')
        self.assertIn('processed', html)
        [self.assertNotIn(keyword, html) for keyword in ['accepted', 'rejected']]


@ddt.ddt
class CustomStudentVerificationPostTest(TestCase):
    """
    Test POST requests to CustomStudentVerification view
    """

    def setUp(self):
        super(CustomStudentVerificationPostTest, self).setUp()
        self.student = User.objects.create(
            username='test-user',
            email='test-user@example.com',
        )
        self.view = CustomStudentVerificationView.as_view()
        self.factory = RequestFactory()

    def tearDown(self):
        super(CustomStudentVerificationPostTest, self).tearDown()
        StudentVerificationRequest.objects.filter(user=self.student).all().delete()
        self.student.delete()

    def test_unautheticated(self):
        request = self.factory.post(
            reverse('custom_student_verification_app:custom-student-verification')
        )
        request.user = AnonymousUser()

        response = self.view(request)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_basic(self):
        request = self.factory.post(
            reverse('custom_student_verification_app:custom-student-verification')
        )
        request.user = self.student
        with open('test_utils/img/test_photo.png', 'rb') as f:
            request = self.factory.post(
                reverse('custom_student_verification_app:custom-student-verification'), {
                    'id_photo': f
                }
            )
            request.user = self.student

        response = self.view(request)
        self.assertEqual(response.status_code, 302)

        request = self.factory.get(
            reverse('custom_student_verification_app:custom-student-verification')
        )
        request.user = self.student
        response = self.view(request)
        html = response.content.decode('utf-8').strip()

        self.assertEqual(response.status_code, 200)
        self.assertNotRegex(html, r'<form .*>')
        self.assertIn('processed', html)
        [self.assertNotIn(keyword, html) for keyword in ['accepted', 'rejected']]

    def test_incorrect_image(self):
        request = self.factory.post(
            reverse('custom_student_verification_app:custom-student-verification')
        )
        request.user = self.student
        with open('test_utils/img/test_corrupted_photo.png', 'rb') as f:
            request = self.factory.post(
                reverse('custom_student_verification_app:custom-student-verification'), {
                    'id_photo': f
                }
            )
            request.user = self.student

        response = self.view(request)
        self.assertEqual(response.status_code, 302)

        request = self.factory.get(
            reverse('custom_student_verification_app:custom-student-verification')
        )
        request.user = self.student
        response = self.view(request)
        html = response.content.decode('utf-8').strip()

        self.assertEqual(response.status_code, 200)
        self.assertRegex(html, r'<form .*>')
        [self.assertNotIn(keyword, html) for keyword in ['accepted', 'rejected', 'processed']]

    def test_previously_accepted(self):
        with patch('custom_student_verification.signals.approve_user') as mock_approve_user:
            StudentVerificationRequest.objects.create(
                user=self.student,
                status="ACCEPTED"
            )
            mock_approve_user.assert_called_with(self.student, None)

        request = self.factory.post(
            reverse('custom_student_verification_app:custom-student-verification')
        )
        request.user = self.student
        with open('test_utils/img/test_photo.png', 'rb') as f:
            request = self.factory.post(
                reverse('custom_student_verification_app:custom-student-verification'), {
                    'id_photo': f
                }
            )
            request.user = self.student

        response = self.view(request)
        self.assertEqual(response.status_code, 302)

        request = self.factory.get(
            reverse('custom_student_verification_app:custom-student-verification')
        )
        request.user = self.student
        response = self.view(request)
        html = response.content.decode('utf-8').strip()

        self.assertEqual(response.status_code, 200)
        self.assertNotRegex(html, r'<form .*>')
        self.assertIn('accepted', html)
        [self.assertNotIn(keyword, html) for keyword in ['processed', 'rejected']]

    def test_previously_pending(self):
        StudentVerificationRequest.objects.create(
            user=self.student,
            status="PENDING"
        )

        request = self.factory.post(
            reverse('custom_student_verification_app:custom-student-verification')
        )
        request.user = self.student
        with open('test_utils/img/test_photo.png', 'rb') as f:
            request = self.factory.post(
                reverse('custom_student_verification_app:custom-student-verification'), {
                    'id_photo': f
                }
            )
            request.user = self.student

        response = self.view(request)
        self.assertEqual(response.status_code, 302)

        request = self.factory.get(
            reverse('custom_student_verification_app:custom-student-verification')
        )
        request.user = self.student
        response = self.view(request)
        html = response.content.decode('utf-8').strip()

        self.assertEqual(response.status_code, 200)
        self.assertNotRegex(html, r'<form .*>')
        self.assertIn('processed', html)
        [self.assertNotIn(keyword, html) for keyword in ['accepted', 'rejected']]

    @patch('custom_student_verification.signals.reject_user')
    def test_previously_rejected(self, mock_method):
        StudentVerificationRequest.objects.create(
            user=self.student,
            status="REJECTED"
        )

        mock_method.assert_called_once_with(self.student, None)

        request = self.factory.post(
            reverse('custom_student_verification_app:custom-student-verification')
        )
        request.user = self.student
        with open('test_utils/img/test_photo.png', 'rb') as f:
            request = self.factory.post(
                reverse('custom_student_verification_app:custom-student-verification'), {
                    'id_photo': f
                }
            )
            request.user = self.student

        response = self.view(request)
        self.assertEqual(response.status_code, 302)

        request = self.factory.get(
            reverse('custom_student_verification_app:custom-student-verification')
        )
        request.user = self.student
        response = self.view(request)
        html = response.content.decode('utf-8').strip()

        self.assertEqual(response.status_code, 200)
        self.assertNotRegex(html, r'<form .*>')
        self.assertIn('processed', html)
        [self.assertNotIn(keyword, html) for keyword in ['accepted', 'rejected']]
