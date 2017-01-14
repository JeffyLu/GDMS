"""GDMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from .views import *
from django.contrib.auth.views import logout

urlpatterns = [
    url(r'^$', index, name='home'),
    url(r'^accounts/login/$', limited_login, name='login'),
    url(r'^accounts/logout/$',logout, name='logout'),
    url(r'^notice/', include('notice.urls')),
    url(r'^student/', include('student.urls')),
    url(r'^teacher/', include('teacher.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^add/$', add),
]
