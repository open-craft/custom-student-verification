"""
django admin pages for StudentVerificationRequest models.
"""
import logging

from django.contrib import admin, messages
from django.db import IntegrityError
from django.utils.translation import ngettext

from .models import StudentVerificationRequest


class StudentVerificationRequestAdmin(admin.ModelAdmin):
    """
    Django admin customizations for CertificateGenerationCourseSetting model.
    """

    list_display = ('name', 'photo_id_tag', 'id_photo', 'status', 'time_created', 'time_modified')
    readonly_fields = ('name', 'user', 'photo_id_tag', 'id_photo', 'time_created', 'time_modified')
    list_filter = ('status',)
    actions = ['mark_student_verification_requests_as_accepted']

    def name(self, obj):
        """
        Return name of the user as stored in their profile.
        """
        return obj.user.profile.name

    def has_delete_permission(self, request, obj=None):
        """
        Disable deletion - Staff members can only change status and reason, not delete.
        """
        return False

    def get_queryset(self, request):
        """
        Prefetch user__profile in the queryset to prevent query explosion when fetching every user's name.
        """
        queryset = super(StudentVerificationRequestAdmin, self).get_queryset(request)
        queryset = queryset.prefetch_related('user__profile')
        return queryset

    def update_fields_for_queryset(self, queryset, field, value):
        """
        Given a queryset, this method will update and save a field with a new value on all its records or rows
        """
        successfully_updated_counter = 0
        failed_to_update_counter = 0
        for record in queryset:
            try:
                setattr(record, field, value)
                record.save()
                successfully_updated_counter += 1
            except IntegrityError as e:
                logging.log(logging.ERROR, e)
                failed_to_update_counter += 1
        return successfully_updated_counter, failed_to_update_counter

    def show_results_to_admin_user(self, request, successfully_updated, failed_to_update):
        """
        Send message to admin view so admin user can visualize if action have run without problem
        """
        self.message_user(
            request,
            ngettext(
                ' %d Student verification request has been successfully updated',
                ' %d Student verification requests have been successfully updated',
                successfully_updated,
            ) % successfully_updated,

        )
        if failed_to_update:
            self.message_user(
                request,
                ngettext(
                    ' %d Student verification request has failed to update',
                    ' %d Student verification requests have failed to update',
                    failed_to_update,
                ) % failed_to_update,
                messages.ERROR
            )

    def mark_student_verification_requests_as_accepted(self, request, queryset):
        """
        Django admin action that change selected student verification requests status to ACCEPTED
        """
        accepted_status = 'ACCEPTED'
        successfully_updated, failed_to_update = self.update_fields_for_queryset(
            queryset.exclude(status=accepted_status),
            'status',
            accepted_status
        )
        self.show_results_to_admin_user(request, successfully_updated, failed_to_update)

    mark_student_verification_requests_as_accepted.short_description = \
        'Mark selected student verification requests as ACCEPTED'


admin.site.register(StudentVerificationRequest, StudentVerificationRequestAdmin)
