from django.conf.urls import url
from django.contrib import admin
from django.urls import include

from eventually import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^eventually/', include('eventually.urls')),
    url(r'^admin/', admin.site.urls),
]
