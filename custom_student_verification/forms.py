"""
Contains UploadIDForm: ModelForm that takes only id_photo: The Photo ID of the student.
"""
from django.forms import ModelForm

from .models import StudentVerificationRequest


class UploadIDForm(ModelForm):
    """
    ModelForm that takes id_photo: The Photo ID image of the Student.
    """

    class Meta:
        """
        Set model & editable fields.
        """

        model = StudentVerificationRequest
        fields = ['id_photo']
