"""TVD URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from Dashboard import views
from django.conf.urls.static import static
from django.conf import settings
from Dashboard.tasks import vehicle_detection

from Dashboard.models import Input

urlpatterns = [
                  url('admin/', admin.site.urls),
                  url('', include('Dashboard.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

all_input = Input.objects.filter(is_processed=False)
for each_input in all_input:
    # vehicle_detection.apply_async(args=[str(each_input.pk)], queue='vehicle_detection')
    vehicle_detection(str(each_input.pk))
