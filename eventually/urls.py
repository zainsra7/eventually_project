from django.conf.urls import url
from eventually import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'about/$', views.about, name='about'),
    url(r'^profile/$',views.profile, name='profile'),
    url(r'^register/$',views.register, name='register'),
    url(r'^dashboard/$',views.dashboard, name='dashboard'),
    url(r'^login/$',views.user_login, name='login'),
    url(r'^logout/$',views.user_logout, name='logout'),
    url(r'^contact/$',views.contact, name='contact'),
    url(r'^search/',views.search,name='search'),
    url(r'^host/$',views.host, name='host'),
    url(r'^event/',views.event, name='event'),
    url(r'^account_confirmation/$',views.account_confirmation, name='account_confirmation'),
]
