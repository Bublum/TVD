from django.conf.urls import url, include
from . import views
from django.views.generic.base import TemplateView

urlpatterns = [
    url(r'^$', views.homepage, name='homepage')
]