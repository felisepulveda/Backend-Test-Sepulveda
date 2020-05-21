from Almuerzos.celery import app
from gestionAlmuerzos.helpers import generar_uuid
from django.conf import settings
from slack import WebClient
from gestionAlmuerzos.models import Menu, Empleado, Pedido, Calendario

SLACK_USER_TOKEN = getattr(settings, 'SLACK_USER_TOKEN', None) # Token del usuario Slack
SLACK_VERIFICATION_TOKEN = getattr(settings, 'SLACK_VERIFICATION_TOKEN', None) # Token para verificar identidad Slack
SLACK_BOT_USER_TOKEN = getattr(settings,'SLACK_BOT_USER_TOKEN', None) # Token de un bot de Slack
MENU_URL = getattr(settings,'MENU_URL', None) # Url del menu del empleado    
ID_CHANNEL = getattr(settings,'ID_CHANNEL', None) #Id del canal donde estan los empleado #gestion-de-almuerzos   
bot_token = WebClient(SLACK_BOT_USER_TOKEN) # bot token
user_token = WebClient(SLACK_USER_TOKEN) # user token

# Esta tarea lista todos los usuarios del canal
@app.task
def listUsersChannel():
    response = user_token.conversations_members(channel=ID_CHANNEL)
    users = response["members"]
    return users

# Esta tarea envia el Slack Reminder
@app.task
def sendReminder():
    users = listUsersChannel()
    for i in users:
        uuid=generar_uuid()
        response = user_token.users_info(user=i)
        real_name = response['user']['real_name']
        user_token.reminders_add(text="Agendar tu almuerzo aca: "+MENU_URL.format(uuid),user=i,time=1)
        addDB(i,uuid,real_name)
    return "ready"

#Esta tarea agrega un empleado a la base de datos, con su uuid y su nombre registrado en Slack
@app.task
def addDB(user,uuid,real_name):
    Em=Empleado(uuid=uuid,nombre=real_name)
    Em.save()


# Esta tarea borra la base de datos diariamente, ya que el proceso de gestionar los almuerzos se hace a diario, y
# el id de un empleado se basa en un uuid, que se genera cada vez que se envia un Slack Reminder a un empleado
@app.task
def drop():
    Pedido.objects.all().delete()
    Empleado.objects.all().delete()


    
