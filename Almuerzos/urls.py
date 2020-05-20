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
#from gestionAlmuerzos.views import Events
from django.contrib.auth import views as v
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('gracias/', views.gracias),
    path('gestion_nora/',login_required(views.gestion_nora),name='gestion_nora'),
    path('consulta_nora/',login_required(views.consulta_nora),name='consulta_nora'),
    path('gestion_pedidos/',login_required(views.gestion_pedidos),name='gestion_pedidos'),
    url('elimina_nora/(?P<i>[0-9a-zA-Z -]+)$',login_required(views.elimina_nora),name='elimina_nora'),
    path('', login_required(views.gestion_nora)),
    url('menu/(?P<uuid>[0-9a-f-]+)$', views.resultado,name='menu'),
    path('menu/', views.resultado),
    #path('events/', Events.as_view()), # En caso que se puedan agregar eventos con robots en Slack
    path('accounts/login/', v.LoginView.as_view(template_name='ingreso.html'),name='login'),
    path('logout/', v.logout_then_login,name='logout'),
    
]
