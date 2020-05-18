"""Almuerzos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import include, path
from django.conf.urls import url
from gestionAlmuerzos import views
from gestionAlmuerzos.views import Events, resultado

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('gestion_nora/', views.gestion_nora),
    #path('resultado/', views.resultado),
    #url(r'^menu/(?P<uuid>[0-9a-f-]+)$', views.consulta),
    #url(r'^menu/(?P<uuid>[0-9a-f-]+)$', resultado.as_view()),
    path('menu/', views.resultado),
    path('events/', Events.as_view()),
]
