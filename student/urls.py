from django.conf.urls import url
from student.views import choose_teacher, my_teacher


urlpatterns = [
    url(r'^choose_teacher$', choose_teacher, name='choose_teacher'),
    url(r'^my_teacher$', my_teacher, name='my_teacher'),
]
