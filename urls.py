#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
#     FileName: urls.py
#         Desc: 2017-03-06 15:06
#       Author: Lu.liu
#        Email: liulou730@163.com
#     HomePage:
#     Function:
# =============================================================================

from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sendemail.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^mail$',views.send_request),
)
