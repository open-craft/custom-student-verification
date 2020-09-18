"""
django admin pages for StudentVerificationRequest models.
"""

from django.contrib import admin

from .models import StudentVerificationRequest


class StudentVerificationRequestAdmin(admin.ModelAdmin):
    """
    Django admin customizations for CertificateGenerationCourseSetting model.
    """

    list_display = ('name', 'photo_id_tag', 'id_photo', 'status', 'time_created', 'time_modified')
    readonly_fields = ('name', 'user', 'photo_id_tag', 'id_photo', 'time_created', 'time_modified')
    list_filter = ('status',)

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


admin.site.register(StudentVerificationRequest, StudentVerificationRequestAdmin)
