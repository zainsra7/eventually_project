from django.confs.urls import url

from eventually import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'about/$', views.about, name='about'),
    url(r'', views)

]