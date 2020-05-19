from django.db import models

# Create your models here.

class Menu(models.Model): #id por defecto
    plato_fuerte=models.CharField(blank=False,max_length=20)
    ensalada=models.CharField(blank=True,max_length=20)
    postre=models.CharField(blank=True,max_length=20)
    #nora=models.ForeignKey(Nora,on_delete=models.CASCADE, null=True)

class Calendario(models.Model):
    fecha=models.DateTimeField(auto_now_add=True,primary_key=True)
    descripcion=models.TextField(blank=True)

class Empleado(models.Model):
    uuid=models.CharField(max_length=50,primary_key=True)
    nombre=models.CharField(blank=False,max_length=40)

class Pedido(models.Model):
    empleado=models.ForeignKey(Empleado,on_delete=models.CASCADE)
    calendario=models.ForeignKey(Calendario,on_delete=models.CASCADE)
    customizacion=models.CharField(blank=True,max_length=20)
    menu=models.ForeignKey(Menu,on_delete=models.CASCADE)

    class Meta:
        unique_together = (('empleado', 'calendario'),)





