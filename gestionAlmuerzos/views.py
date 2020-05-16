from django.shortcuts import render
from django.http import HttpResponse
from gestionAlmuerzos.models import Menu

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from slack import WebClient
from django.conf import settings


# Create your views here.

def gestion_nora(request):

    return render(request,"gestion_nora.html")

def resultado(request):

    if request.method=='plato_fuerte':
        mensaje="menu: %r" %request.POST['plato_fuerte']

    else:
        mensaje="No has ingresado nada"
    return HttpResponse(mensaje)


def consulta(request):

    if request.method=='POST':

        slack_response="hola"

        return render(request,"menu.html",{"slack_response":slack_response})

    return render(request,"menu.html")





SLACK_VERIFICATION_TOKEN = getattr(settings, 'SLACK_VERIFICATION_TOKEN', None)
SLACK_BOT_USER_TOKEN = getattr(settings,'SLACK_BOT_USER_TOKEN', None)              
Client = WebClient(SLACK_BOT_USER_TOKEN)

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
                Client.chat_postMessage(channel=channel,text=bot_text)
                return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_200_OK)

    
    
