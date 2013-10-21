from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^wStationMgr/', include('wStationMgr.urls', namespace="wStationMgr")),
    url(r'^wStationMgr/api/', include('rest_framework.urls', namespace='rest_framework')),    
    url(r'^wStationMgr/admin/', include(admin.site.urls)),
)

