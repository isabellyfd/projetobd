# -*- coding: utf-8 -*-
"""sistemapsc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from psc_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.inscricao, name = 'inscricao'),
    url(r'^login', views.login_admin, name = 'login'),
    url(r'^logar', views.logar_admin, name = 'logar'),
    url(r'^logout', views.logout_admin, name = 'logout'),
    url(r'^inscrever', views.inscrever, name = 'inscrever'),
    url(r'^minha-inscricao', views.editar_inscrito, name = 'editar_inscricao'),
    url(r'^editar-admin/(?P<id>[0-9]+)', views.editar_admin, name = 'editar_admin'),
    url(r'^ver-admin/(?P<id>[0-9]+)', views.ver_admin, name = 'ver_admin'),
    url(r'^save-inscrito/(?P<id>[0-9]+)', views.salvar_edicao, name = 'salvar_edicao'),
    url(r'^enviar-email/(?P<id>[0-9]+)', views.enviar_email, name = 'enviar_email'),
    url(r'^cadastrar-periodo', views.cadastrar_periodo, name = 'cadastrar_periodo'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
