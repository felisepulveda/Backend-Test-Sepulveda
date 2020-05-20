# Librerias nativas
from datetime import date, datetime, time

# Librerias mias
from gestionAlmuerzos.models import Menu, Empleado, Pedido, Calendario
from gestionAlmuerzos.tasks import sendReminder, drop
from gestionAlmuerzos.helpers import generar_uuid

# Librerias de Django y de la api Slack
from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from slack import WebClient
from slack.errors import SlackApiError

# Variables de entorno
SLACK_USER_TOKEN = getattr(settings, 'SLACK_USER_TOKEN', None) # Token del usuario Slack
SLACK_VERIFICATION_TOKEN = getattr(settings, 'SLACK_VERIFICATION_TOKEN', None) # Token para verificar identidad Slack
SLACK_BOT_USER_TOKEN = getattr(settings,'SLACK_BOT_USER_TOKEN', None) # Token de un bot de Slack  
MENU_URL = getattr(settings,'MENU_URL', None) # Url del menu del empleado          
bot_token = WebClient(SLACK_BOT_USER_TOKEN) # bot token
user_token = WebClient(SLACK_USER_TOKEN) # user token

# Creacion de todas mis vistas
# Todo el sistema tiene su debido sistema de autentificacion.  
# Sin autentificarse, ninguna url intermedia es accesible (gestion_nora.html,consulta_nora.html,elimina_nora.html,
# gestion_pedidos.html),
# excepto las vistas relacionadas con el slack reminder, que no requieren autentificacion (menu.html,gracias.html)


# Aca Nora puede gestionar toda su operacion, es decir, ingresa menus, consulta menus, consulta pedidos.
def gestion_nora(request):
    if request.method=='POST':
        search = [request.POST.get('plato_fuerte'),request.POST.get('ensalada'),request.POST.get('postre')]
        if search[0] or search[1] or search[2]:
            Me=Menu.objects.filter(plato_fuerte=search[0],ensalada=search[1],postre=search[2])
            if Me: # Si la encuentra, no la debe agregar
                mensaje="Este menu ya fue ingresado, porfavor ingrese otro"
                #mensaje="menu: %r" %request.POST['plato_fuerte']
                return render(request,"gestion_nora.html",{"mensaje":mensaje})
            else: # Si no la encuentra, la debe agregar
                Me=Menu(plato_fuerte=search[0],ensalada=search[1],postre=search[2])
                Me.save()
                mensaje="menu:{}, {}, {} registrado con fecha {}".format(search[0],search[1],search[2],date.today()) 
                return render(request,"gestion_nora.html",{"mensaje":mensaje})  
        else:
            mensaje = "Debe ingresar algo"
            return render(request,"gestion_nora.html",{"mensaje":mensaje})  
    else:
        return render(request,"gestion_nora.html",{"mensaje:": "Ingresa tu Menu del dia"})


# Aca Nora puede gestionar sus pedidos
def gestion_pedidos(request):
    Ped=Pedido.objects.all()
    if Ped:
        mensaje = { 
        "data" : [], 
        } 
        for i in Ped:
            mensaje['data'].append(i)
        return render(request,"gestion_pedidos.html",mensaje) 
    else:
        mensaje="Aun no registra pedidos ingresados"
        return render(request,"gestion_pedidos.html",{"msj" : mensaje})


# Aca Nora puede gestionar sus menus
def consulta_nora(request):
    Me=Menu.objects.all()
    if Me: # si encuentra menus, los retorna
        mensaje = { 
        "data" : [], 
        } 
        for i in Me:
            mensaje['data'].append(i)
        return render(request,"consulta_nora.html",mensaje) 
    else: # si no encuentra, retorna mensaje diciendo que no hay
        mensaje="Usted no ha ingresado ningun menu"
        return render(request,"consulta_nora.html",{"msj" : mensaje})    

# Aca Nora puede eliminar menus
def elimina_nora(request,i):
    menus=i.split('-')
    Me=Menu.objects.filter(plato_fuerte=menus[0],ensalada=menus[1],postre=menus[2])
    if Me: # Si la encuentro la debo eliminar
        Me=Menu.objects.get(plato_fuerte=menus[0],ensalada=menus[1],postre=menus[2])
        Me.delete()
    mensaje = "Menu "+menus[0]+' '+menus[1]+' '+menus[2]+" eliminado"
    return render(request,"elimina_nora.html",{"mensaje" :mensaje})  

# vista de agradecimiento, que informa al empleado que su pedido fue registrado exitosamente
def gracias(request):
    if request.method=='POST': 
        menu=request.POST['seleccion']
        empleado=request.POST['uuid']
        customizacion=request.POST['customizacion']
        tiempolimite=time(11,0,0) # Esta es la hora limite de cornershop 11 AM CLT
        #fecha=date.today() extrae 2020-05-19
        #hora=datetime.time(datetime.now()) extrae 21:59:07.608396
        if datetime.time(timezone.localtime(timezone.now())) <= tiempolimite : # Verifico si cumplo el limite de tiempo, antes de las 11:00
            DateTime=timezone.localtime(timezone.now())
            Date=datetime.date(DateTime)
            Ped=Pedido.objects.filter(empleado=empleado,calendario=Date) # Busco si está este pedido
            if Ped: # Si esta
                print (Ped)
                mensaje="Lo sentimos, usted ya tiene un menu ingresado: {}".format(str(Ped[0]))
            else: # No esta, lo debo ingresar
                Cal=Calendario(fecha=Date,descripcion="Hoy Norita tenia promocion en sus precios")
                Cal.save()
                Ped=Pedido(empleado_id=empleado,calendario_id=Date,fechaHora=DateTime,customizacion=customizacion,menu_id=menu)
                Ped.save()
                mensaje="Menu ingresado, gracias por confiar en Norita"
        else:
            mensaje="Lo sentimos, pero el limite para hacer tu pedido es hasta las 11:00, intenta mañana"
        return render(request,"gracias.html",{"mensaje":mensaje})
    else:
        return render(request,"gracias.html")


# Aca el empleado puede seleccionar el menu de su eleccion, y agregar customizaciones
def resultado(request,uuid=0):
    Me=Menu.objects.all()
    Em=Empleado.objects.filter(uuid=uuid)
    if Em: # si el empleado existe, significa que su slack reminder fue registrado, y aun no estamos en el dia siguiente
        if Me:
            Em=Empleado.objects.get(uuid=uuid)
            menus = {'id' : [], 'plato_fuerte' : [], 'ensalada' : [], 'postre' : []}
            dictMe = { 
                "data" : [], 
                }
            j=0    
            for i in Me:
                    dictMe['data'].append(i)
                    aux=str(dictMe['data'][j]).split('-')
                    clave_primaria=Menu.objects.get(plato_fuerte=aux[0],ensalada=aux[1],postre=aux[2])
                    menus['id'].append(clave_primaria.id)
                    menus['plato_fuerte'].append(aux[0])
                    menus['ensalada'].append(aux[1])
                    menus['postre'].append(aux[2])
                    j=j+1 
            lst = [{'item1': t[0], 'item2': t[1], 'item3':t[2], 'item4':t[3]} for t in zip(menus['id'],menus['plato_fuerte'],menus['ensalada'],menus['postre'])]     
            return render(request,"menu.html",{"menus": lst, "uuid": uuid, "nombre": Em.nombre})
        else:
            mensaje="No existe menu ingresado"
            return render(request,"menu.html",{"mensaje": mensaje})
    else: # si empleado no existe, entonces ya estamos en el dia siguiente, porque la base de datos se actualizo con crontabs
        mensaje="Su pedido ya expiro"
        return render(request,"menu.html",{"mensaje": mensaje})




    
    
