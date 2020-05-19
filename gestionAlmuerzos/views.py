import time
import json
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import CreateView, ListView
from gestionAlmuerzos.models import Menu
from gestionAlmuerzos.tasks import sendReminder

from gestionAlmuerzos.helpers import generar_uuid

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from slack import WebClient
from slack.errors import SlackApiError
from django.conf import settings

SLACK_USER_TOKEN = getattr(settings, 'SLACK_USER_TOKEN', None)
SLACK_VERIFICATION_TOKEN = getattr(settings, 'SLACK_VERIFICATION_TOKEN', None)
SLACK_BOT_USER_TOKEN = getattr(settings,'SLACK_BOT_USER_TOKEN', None)   
MENU_URL = getattr(settings,'MENU_URL', None)            
bot_token = WebClient(SLACK_BOT_USER_TOKEN) # bot token
user_token = WebClient(SLACK_USER_TOKEN) # user token

# Create your views here.

"""def ingreso(request):
    if request.method=='POST':
        miForm=FormularioIngreso(request.POST)
        if miForm.is_valid():
            infForm=miForm.cleaned_data
            checkear=Nora.objects.filter(nombre=infForm['nombre'],password=infForm['password'])
            if checkear:
                #print (checkear[0])
                return render(request,"gestion_nora.html")
                #return HttpResponse("gestion_nora.html")
            else:
                return render(request,"ingreso.html",{"form":miForm,"men":"Usted no es norita, intente nuevamente"})
        else:
            return render(request,"ingreso.html")
    else:
        miForm=FormularioIngreso()
    return render(request,"ingreso.html",{"form":miForm})"""


def gestion_nora(request):

    if request.method=='POST':
        if request.POST.get('plato_fuerte') is not None:
            mensaje="menu: %r" %request.POST['plato_fuerte']
            return render(request,"gestion_nora.html",{"mensaje":mensaje})
        else:
            try:
                sendReminder.delay()
                slack_response="mensaje posteado"
                return render(request,"gestion_nora.html",{"slack_response":slack_response})
                    

            except SlackApiError as e:
                # You will get a SlackApiError if "ok" is False
                #assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
                print (e.response["error"])

    else:
        return render(request,"gestion_nora.html")
    


def resultado(request,uuid):
    #print (json.loads(request.body.decode("utf-8")))
    print (type(uuid))
    print (uuid)
    if request.method=='POST':
            mensaje="Menu ingresado"

    else:
            mensaje="No has ingresado nada"
    return render(request,"menu.html",{"mensaje":mensaje})


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

    
    
