"""
Definition of urls for TaskScheduler.
"""

from datetime import datetime
from django.conf.urls import url, include
from django.contrib import admin
import django.contrib.auth.views

import app.forms
import app.views

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [

	url(r'^admin', include(admin.site.urls)),
	url(r'^scheduler/', include("task_scheduler.urls")),
    
]
