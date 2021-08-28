"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, re_path, include
from django.conf import settings
from django.views.static import serve
from django.contrib.auth import logout
from customer.views import signin, signout, first_step, second_step, third_step, cabinet, checkin, get_flight_date, count_total_price, available_seat


urlpatterns = [
    path('admin/', admin.site.urls),
    path('signin/', signin, name='signin'),
    path('logoff/', signout, name='signout'),
    path('cabinet/', cabinet, name='cabinet'),
    path('checkin/', checkin, name='checkin'),
    path('', first_step, name='first_step'),
    path('second_step/', second_step, name='second_step'),
    path('third_step/', third_step, name='third_step'),
    path('get_flight_date/', get_flight_date, name='get_flight_date'),
    path('available_seat/', available_seat, name='available_seat'),
    path('count_total_price/', count_total_price, name='count_total_price'),
    path('', include('social_django.urls', namespace='social')),
    re_path(r'static/(?P<path>.*)$', serve, {'document_root':settings.STATIC_ROOT}),
    re_path(r'media/(?P<path>.*)$', serve, {'document_root':settings.MEDIA_ROOT}),
]
