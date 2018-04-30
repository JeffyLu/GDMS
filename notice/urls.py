from django.conf.urls import url
from notice.views import notice, detail


urlpatterns = [
    url(r'^$', notice, name='notice'),
    url(r'^([1-9][0-9]*)$', detail, name='detail'),
]
