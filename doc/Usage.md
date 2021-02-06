# Using Custom Student Verification App

## Theme Customization

To use this app you need to customize/override some templates in your custom theme. To know more about edX comprehensive theming, [check here](https://edx.readthedocs.io/projects/edx-installing-configuring-and-running/en/latest/ecommerce/theming.html).

- ``lms/templates/verify_student/incourse_reverify.html``
- ``lms/templates/verify_student/pay_and_verify.html``
- ``lms/templates/verify_student/reverify_not_allowed.html``
- ``lms/templates/verify_student/reverify.html``

Override these templates by copying ``verify_student`` template directory to ``your-theme/lms/templates`` directory. Look at changes in ``content`` block from [these examples](templates/verify_student).

## Submitting Identification Document

Once installed and enabled, learners should see the following identification document upload form when trying to verify themselves -

![File Upload UI](img/file-upload-ui.png)

Learners should upload their identification documents via this form. After uploading the document they will see a confirmation message -

![Verification Request Submitted](img/verification-request-submitted.png)


## Approving Verification Request

Administrators can approve or reject verification requests submitted by learners via LMS Django Admin Panel.

![Django Admin](img/django-admin.png)

They will see a list of verification requests with status and uploaded document -

![Verification Requests List](img/verification-request-list.png)

Then, they can approve or reject any request from the edit view -

![Accept or Reject Request](img/accept-reject-request.png)
