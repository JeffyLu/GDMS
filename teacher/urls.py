from django.conf.urls import url
from teacher.views import my_student


urlpatterns = [
    url(r'^my_student$', my_student, name='my_student'),
]
