from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns=[
    url(r'^$', views.home, name='home'),
    url(r'^signup/', views.register, name='signup'),
    url(r'^user/(?P<username>\w+)', views.profile, name='profile'),
    url(r'^edit/', views.edit_profile, name='edit_profile'),
    url(r'^upload/$', views.upload_designs, name='upload_designs'),

]



