from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.views import login
from wStationMgr import views

urlpatterns = patterns('wStationMgr.views',    
    url(r'^tree/(?P<node_id>\d+)/$', login_required( views.tree ), name='tree'),    
    url(r'^tree_json/(?P<node_id>\d+)/$', views.tree_json, name='tree_json'),    
    url(r'^help/$', views.help, name='help'),    
    url(r'^$', login_required( views.IndexView.as_view()), name='index'),
    
    # API
    url(r'^api/$', views.NodeList.as_view() ),
    url(r'^api/(?P<node_id>[0-9]+)/$', views.NodeDetail.as_view() ),
    url(r'^api/data/(?P<node_id>[0-9]+)/$', views.DataDetail.as_view() ),
    url(r'^api/data/$', views.DataList.as_view() ),
    url(r'^api/server/$', views.ServerList.as_view() ),
    url(r'^api/network/$', views.NetworkList.as_view() ),
    url(r'^api/ldevice/$', views.LogicalDeviceList.as_view() ),
    url(r'^api/lnode/$', views.LogicalNodeList.as_view() ),

    # Login / logout.
    url(r'^login/$', login),
    url(r'^logout/$', views.logout_page, name='logout_page'),    
)



