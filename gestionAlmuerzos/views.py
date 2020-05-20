from datetime import date, datetime, time

from gestionAlmuerzos.models import Menu, Empleado, Pedido, Calendario
from gestionAlmuerzos.tasks import sendReminder, drop
from gestionAlmuerzos.helpers import generar_uuid

from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from slack import WebClient
from slack.errors import SlackApiError

SLACK_USER_TOKEN = getattr(settings, 'SLACK_USER_TOKEN', None)
SLACK_VERIFICATION_TOKEN = getattr(settings, 'SLACK_VERIFICATION_TOKEN', None)
SLACK_BOT_USER_TOKEN = getattr(settings,'SLACK_BOT_USER_TOKEN', None)   
MENU_URL = getattr(settings,'MENU_URL', None)            
bot_token = WebClient(SLACK_BOT_USER_TOKEN) # bot token
user_token = WebClient(SLACK_USER_TOKEN) # user token

# Create your views here.

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
        try:
            #drop.delay()
            #sendReminder.delay()
            mensaje="slack posteado"
            return render(request,"gestion_nora.html",{"mensaje":mensaje})
                    

        except SlackApiError as e:
                # You will get a SlackApiError if "ok" is False
                #assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
                print (e.response["error"])
        return render(request,"gestion_nora.html",{"mensaje:": "Ingresa tu Menu del dia"})
    

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

def elimina_nora(request,i):
    #print (i)
    menus=i.split('-')
    Me=Menu.objects.filter(plato_fuerte=menus[0],ensalada=menus[1],postre=menus[2])
    if Me: # Si la encuentro la debo eliminar
        Me=Menu.objects.get(plato_fuerte=menus[0],ensalada=menus[1],postre=menus[2])
        Me.delete()
    mensaje = "Menu "+menus[0]+' '+menus[1]+' '+menus[2]+" eliminado"
    return render(request,"elimina_nora.html",{"mensaje" :mensaje})  


def gracias(request):
    if request.method=='POST': 
        menu=request.POST['seleccion']
        empleado=request.POST['uuid']
        customizacion=request.POST['customizacion']
        tiempolimite=time(11,0,0)
        #fecha=date.today() extrae 2020-05-19
        #hora=datetime.time(datetime.now()) extrae 21:59:07.608396
        if datetime.time(datetime.now()) <= tiempolimite : # Verifico si cumplo el limite de tiempo, antes de las 11:00
            DateTime=datetime.now()
            Date=datetime.date(DateTime)
            print (DateTime)
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

def resultado(request,uuid=0):
    Me=Menu.objects.all()
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


def consulta(request):

    if request.method=='POST':
        try:
            response = bot_token.users_list()
            users = response["members"]
            user_ids = list(map(lambda u: u["id"], users))
            #print (user_ids)
            for i in user_ids:
                if i not in ['USLACKBOT','U01410U5Z6V']:
                    #bot_token.chat_postMessage(channel="C0136160H0X",text="Hello from your app! :tada:")
                    #bot_token.chat_postMessage(channel=i,text="Hello from your app! :tada:")
                    #bot_token.chat_scheduleMessage(channel=i,text="Hola, te recuerdo que debes terminar esto",post_at=time.time()+20)
                    user_token.reminders_add(text="www.google.cl",user=i,time=1)
                    slack_response="mensaje posteado"
                    return render(request,"menu.html",{"slack_response":slack_response})
                else:
                    continue

        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            #assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
            print (e.response["error"])
    return render(request,"menu.html")







class Events(APIView):
    def post(self, request, *args, **kwargs):
        slack_message = request.data
        #print (slack_message)
        if slack_message.get('token') != SLACK_VERIFICATION_TOKEN:
            return Response(status=status.HTTP_403_FORBIDDEN)

        # verification challenge
        if slack_message.get('type') == 'url_verification':        
            return Response(data=slack_message,status=status.HTTP_200_OK)

        # greet bot
        if 'event' in slack_message:                              
            event_message = slack_message.get('event')            
            
            # ignore bot's own message
            #if event_message.get('subtype') == 'bot_message':     
            if event_message.get('bot_id'):   
                return Response(status=status.HTTP_200_OK)        
            
            # process user's message
            user = event_message.get('user')
            text = event_message.get('text')
            channel = event_message.get('channel')
            bot_text = 'Hola PIPO <@{}> :wave:'.format(user)
            if 'hola robot sexy' in text.lower():
                #Client.api_call(api_method='chat.postMessage',channel=channel,text=bot_text)
                bot_token.chat_postMessage(channel=channel,text=bot_text)
                return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_200_OK)

    
    
