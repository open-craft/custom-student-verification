# Using Custom Student Verification App

## Theme Customization

To use this app you need to customize/override some templates in your custom theme. To know more about edX comprehensive theming, [check here](https://edx.readthedocs.io/projects/edx-installing-configuring-and-running/en/latest/configuration/changing_appearance/theming/index.html).

Copy following files -
- ``lms/templates/verify_student/incourse_reverify.html`` to ``<YOUR-THEME>/lms/templates/verify_student/incourse_reverify.html``.
- ``lms/templates/verify_student/pay_and_verify.html`` to ``<YOUR-THEME>/lms/templates/verify_student/pay_and_verify.html``.
- ``lms/templates/verify_student/reverify.html`` to ``<YOUR-THEME>/lms/templates/verify_student/reverify.html``.

On the top of those files import ``reverse`` as it will be used later -
```
<%!
from django.utils.translation import ugettext as _
from django.urls import reverse
%>
```

Then change the ``content`` block for each of those files as -
```html

<%block name="content">

<div id="error-container" style="display: none;"></div>

<div class="container">
    <!-- This iframe will embed custom verification UI in LMS-->
    <iframe src="${reverse('custom_student_verification_app:custom-student-verification')}" style="width:100%;height:100%;border: 0;"></iframe>

</div>

```


Copy ``lms/templates/verify_student/reverify_not_allowed.html`` to ``<YOUR-THEME>/lms/templates/verify_student/reverify_not_allowed.html``. And, change the ``instructions`` section in the ``content`` block as following -

```html
<div class="instructions">
    <p>
        % if status is "approved":
            ${_("Your Identity Verification has been approved.")}
        % elif status is "pending":
            ${_("You have already submitted your verification information. You will see a message on your dashboard when the verification process is complete (usually within 5-7 days).")}
        % else:
            ${_("You cannot verify your identity at this time.")}
        % endif
    </p>
</div>
```

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
