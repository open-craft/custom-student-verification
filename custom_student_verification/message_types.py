"""
ACE message types for the custom_student_verfication app.
"""
from custom_student_verification.compat import get_base_message_type

BaseMessageType = get_base_message_type()


class VerificationApproved(BaseMessageType):
    """
    A message to the learner when their ID verification has been approved.
    """

    APP_LABEL = 'custom_student_verification'
    NAME = 'verificationapproved'

    def __init__(self, *args, **kwargs):
        """Init method."""
        super().__init__(*args, **kwargs)
        self.options['transactional'] = True


class VerificationRejected(BaseMessageType):
    """
    A message to the learner when their ID verification has been rejected.
    """

    APP_LABEL = 'custom_student_verification'
    NAME = 'verificationrejected'

    def __init__(self, *args, **kwargs):
        """Init method."""
        super().__init__(*args, **kwargs)
        self.options['transactional'] = True
