from django.conf.urls import url
from . import views

app_name = 'detection'

urlpatterns = [
    url(r'^home$', views.homepage, name='homepage'),
    url(r'^violation$', views.violation, name='violation'),
    url(r'^daywise$', views.daywise, name='daywise'),
]