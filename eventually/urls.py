from django.conf.urls import url
from eventually import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'about/$', views.about, name='about'),
    url(r'^user_profile/$',views.user_profile, name='user_profile'),
    url(r'^register/$',views.register, name='register'),
    url(r'^dashboard/$',views.dashboard, name='dashboard'),
    url(r'^login/$',views.user_login, name='login'),
    url(r'^logout/$',views.user_logout, name='logout'),
    url(r'^contact/$',views.contact, name='contact'),
    url(r'^search/$',views.search,name='search'),
    url(r'^host/$',views.host, name='host'),
    url(r'^event/(?P<event_id>[\w\-]+)/$',views.event, name='event'),
    url(r'^join/$',views.join_event, name='join_event'),
    url(r'^forget_password/$', views.forget_password, name="forget_password")
]