from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
import views

urlpatterns = [

]
if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)