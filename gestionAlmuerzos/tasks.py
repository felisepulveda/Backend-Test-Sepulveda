from Almuerzos.celery import app
from gestionAlmuerzos.helpers import generar_uuid
from django.conf import settings
from slack import WebClient
from gestionAlmuerzos.models import Menu, Empleado, Pedido, Calendario

SLACK_USER_TOKEN = getattr(settings, 'SLACK_USER_TOKEN', None)
SLACK_VERIFICATION_TOKEN = getattr(settings, 'SLACK_VERIFICATION_TOKEN', None)
SLACK_BOT_USER_TOKEN = getattr(settings,'SLACK_BOT_USER_TOKEN', None)   
MENU_URL = getattr(settings,'MENU_URL', None)       
ID_CHANNEL = getattr(settings,'ID_CHANNEL', None)     
bot_token = WebClient(SLACK_BOT_USER_TOKEN) # bot token
user_token = WebClient(SLACK_USER_TOKEN) # user token


@app.task
def listUsersChannel():
    response = user_token.conversations_members(channel=ID_CHANNEL)
    users = response["members"]
    return users

@app.task
def sendReminder():
    users = listUsersChannel()
    for i in users:
        uuid=generar_uuid()
        response = user_token.users_info(user=i)
        real_name = response['user']['real_name']
        user_token.reminders_add(text=MENU_URL.format(uuid),user=i,time=1)
        addDB(i,uuid,real_name)
    return "ready"

#Empleado.objects.filter(uuid=uuid)  es el where 
#Em=Empleado(uuid='',nombre='') es el insert
#Em.save()
#Em=Empleado.objects.get(uuid=uuid) es el delete
#Em.delete()

@app.task
def addDB(user,uuid,real_name):
    Em=Empleado(uuid=uuid,nombre=real_name)
    Em.save()


@app.task
def drop():
    Pedido.objects.all().delete()
    Empleado.objects.all().delete()
    Menu.objects.all().delete()


    
