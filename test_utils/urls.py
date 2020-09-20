from django.conf.urls import url
from django.urls import include

app_name = "test"

urlpatterns = [
    url(r'', include(
        ('custom_student_verification.urls', 'custom_student_verification'),
        namespace="custom_student_verification_app")
        ),
]
