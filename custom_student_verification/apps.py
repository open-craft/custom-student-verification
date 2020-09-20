# -*- coding: utf-8 -*-
# pylint: disable=import-outside-toplevel
"""
custom_student_verification Django application initialization.
"""

from __future__ import absolute_import, unicode_literals

from django.apps import AppConfig


class CustomStudentVerificationConfig(AppConfig):
    """
    Configuration for the custom_student_verification Django application.
    """

    name = 'custom_student_verification'
    plugin_app = {
        'url_config': {
            'lms.djangoapp': {
                'namespace': 'custom_student_verification_app',
            },
        },
    }

    def ready(self):
        """
        Set up signals for app.
        """
        from custom_student_verification import signals  # pylint: disable=unused-import
