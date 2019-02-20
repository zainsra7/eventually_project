from django.conf.urls import url
from eventually import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'about/$', views.about, name='about'),
    url(r'register/$', views.register, name='register'),
    url(r'account_confirmation/$', views.account_confirmation, name='account_confirmation'),
    url(r'login/$', views.user_login, name='login'),
    url(r'forgot_password/$', views.forgot_password, name='forgot_password'),
    url(r'password_reset/$', views.password_reset, name='password_reset'),
    url(r'sign_out/$', views.sign_out, name='sign_out'),
]
