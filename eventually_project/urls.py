from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from eventually import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^eventually/', include('eventually.urls')),
    url(r'^admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)