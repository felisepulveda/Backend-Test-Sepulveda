## Preparación ambiente de trabajo, todo fue realizado en windows 10
Paquetes necesarios

- virtualenv 16.1.0
- virtualenvwrapper-win 1.2.5
- gevent 20.5.0 
- psycopg2 2.8.5 
- redis 3.5.2 
- Django 3.0.6 
- django-slack-app 1.0.40 
- django-celery-beat 2.0.0 
- django-celery-results 1.2.1 
- djangorestframework 3.11.0 
- coverage 5.1 
- django-nose 1.4.6 

Ahora, instalamos Python 3.6.2, abrimos una terminal, e instalamos los siguientes paquetes
- pip install virtualenv==16.1.0
- pip install virtualenvwrapper-win==1.2.5

Luego en la misma terminal, escribimos lo siguiente
- 'mkvirtualenv Nora'  (Acá creas el ambiente virtual llamado 'Nora', e ingresas a él automáticamente)

Crea una carpeta con el mismo nombre del ambiente, es decir, 'Nora', e ingresa a ella en tu terminal y escribe lo siguiente
- 'setprojectdir .' (ahora cada vez que ingresemos a nuestro ambiente, nos dirigira a la carpeta 'Nora')
- 'workon Nora' (para ingresar al ambiente, 'deactivate' es para salir)

Clonamos mi repositorio dentro de 'Nora', y nos situamos al mismo nivel del archivo manage.py dentro de nuestra cmd.

Ahora instalamos paquetes de python con el comando
- pip install -r requerimientos.txt 

## Sistema de gestión de base de datos
Usamos postgresql como nuestro sistema de base de datos, por tanto, debe 
1) Abrir postgresql, y crear su base de datos con 'el nombre que quiera'
2) Se debe configurar en el archivo settings.py del proyecto los valores 
<pre>
- DATABASES = {        
    'default': {     
        'ENGINE': 'django.db.backends.postgresql_psycopg2',    
        'NAME': 'el nombre que quiera', # Nombre de la base de datos    
        'USER': 'postgres',	# Aca      
        'PASSWORD': 'root',     # Aca        
        'HOST': 'localhost',	# Dependiendo en que servidor se almacena su sistema de gestion de base de datos     
        'DATABASE': '5432',	# El puerto del servidor    
    }       
}         
</pre>
## Ejecución Proyecto
Para ejecutar nuestro proyecto Almuerzos, escribimos los siguientes comandos en nuestro ambiente 'Nora' (al mismo nivel archivo manage.py)
- python manage.py makemigrations
- python manage.py migrate
- python manage.py createsuperuser (Creamos a nora con todos los permisos, aunque se puede cambiar en caso de asi desearlo)
[username: nora, email: 'xxx@gmail.com', password: nora1234567] 

Luego, descargamos e instalamos ngrok, y ejecutamos ngrok.exe, se abrirá una terminal y escribimos 
- ngrok http 80 (servidor tunel)

Luego, en el archivo settings.py copiamos la url generada por ngrok 'https://xxxxxxxx.ngrok.io' en
<pre>
- ALLOWED_HOSTS =[],
- MENU_URL = 'https://xxxxxxxx.ngrok.io/menu/{}',
</pre>

Luego, en nuestro ambiente virtual 'Nora' escribimos
- python manage.py runserver 0.0.0.0:80  (servidor django, '0.0.0.0:80' correra a traves de ngrok)

#### Pueden solo correr 'python manage.py runserver', ya que asumo tienen la URL 'https://nora.cornershop.io' para probar el programa,
en este caso, al final del archivo settings.py de nuestro proyecto Almuerzos deben
<pre>
- #MENU_URL = 'https://nora.cornershop.io/menu/{}'	DESCOMENTAR
- MENU_URL = 'https://xxxxxxxx.ngrok.io/menu/{}'	COMENTAR
</pre>

Luego descargamos redis para windows, y abrimos redis-server.exe, se nos abrirá una terminal, y escribimos
- redis-server (servidor redis)

Luego abrimos dos terminales mas (en ambiente 'Nora', al nivel de manage.py), y escribimos

Terminal 1
- celery worker -A Almuerzos.celery --loglevel=info -P gevent (comando de celery para workers)

Terminal2
- celery -A Almuerzos.celery beat --loglevel=INFO --pidfile= 
(comando de celery beat para crontabs,--pidfile= es para que no crees tu archivo pidfile, si no lo escribes, en la proxima ejecucion debes referenciar ese archivo)

## Credenciales Slack
Crear una app en slack, y con los siguientes scopes para 'user'
- channels:read
- reminders:write
- users:read

En el archivo Almuerzos/Almuerzos/settings.py copia lo siguiente
<pre>
- SLACK_USER_TOKEN = 'xoxp-xxxxxxxxxxxxxx-xxxxxxxxxxxxxx-xxxxxxxxdxxxxxxxxxxxxxxx'
- ID_CHANNEL = 'CXXXXXXXXXX' (Tu canal puede llamarse como quieras, pero en él deben estar todos los empleados al que quieres entregar almuerzos)
</pre>

## Credenciales para Nora
- Username: nora
- Password: nora1234567

## Pruebas 
Para generar un reporte, escribir

- python manage.py test   (viene integrado django-nose y coverage)

## Explicación
Nuestro programa borra la base datos diariamiente (tabla empleados y tabla pedidos) a las 6:15 AM, ya que simulamos una base de datos en cache,
y los uuid son generados on the fly. Los slack reminders se envian a las 7:15 AM. Todo esto se hace gracias a celery y redis de forma asincrona.
No se pueden hacer pedidos despues de las 11 AM. El comportamiento del borrado de la base de datos se puede impedir simplemente eliminando borrar_db en el 
'CELERYBEAT_SCHEDULE' de celery.py. Se usan sistemas de autentificacion, se bloquean URLs intermedias, excepto las relacionadas con la selección de almuerzos 
de los empleados. El codigo impide ciertas inconsistencias como ingresar menus con campos en blancos, que el empleado pida mas de un menu al dia, que no pueda pedir menus
si es que a Nora se le olvido agregar un menu diario, y borro sus menus registrados, etc. 

## Autocrítica
1) Use postgresql, la cual considero debe ser usada para proyectos muy grandes, pense en la escalabilidad de la app, pero al final, es como matar una mosca con una bazuca.
2) Queria hacer mas testing, pero estuve ajustado de tiempo.
3) Se que deje algunas credenciales privadas de Slack en mi código, pero ya tenia mi repo reprobado, y no quería sacar algo y que despues no funcionara.
4) Si por alguna razón, algo no llegara a funcionar, solo contactarme, porque si funciona, pero siempre puede pasa algo.
5) A Nora le di permisos de super usuaria, asi que técnicamente, podría ingresar a django/admin. Esto se puede cambiar, disminuyendo los permisos.
A probar nomas!!!!!. Saludos, y gracias por la oportunidad.
