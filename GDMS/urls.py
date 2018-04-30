from django.conf.urls import url, include
from django.contrib import admin
from GDMS.views import index, limited_login, add
from django.contrib.auth.views import logout


urlpatterns = [
    url(r'^$', index, name='home'),
    url(r'^accounts/login/$', limited_login, name='login'),
    url(r'^accounts/logout/$', logout, name='logout'),
    url(r'^notice/', include('notice.urls')),
    url(r'^student/', include('student.urls')),
    url(r'^teacher/', include('teacher.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^add/$', add),
]
