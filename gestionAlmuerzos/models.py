from django.db import models

# Create your models here.

class Menu(models.Model): #id por defecto
    #menu_id=models.IntegerField(primary_key=True)
    plato_fuerte=models.CharField(blank=False,max_length=30)
    ensalada=models.CharField(blank=True,max_length=30)
    postre=models.CharField(blank=True,max_length=30)
    #nora=models.ForeignKey(Nora,on_delete=models.CASCADE, null=True)
    def __str__(self):
        return '%s-%s-%s' % (self.plato_fuerte,self.ensalada,self.postre)

class Calendario(models.Model):
    fecha=models.DateField(primary_key=True)
    descripcion=models.TextField(blank=True)

class Empleado(models.Model):
    uuid=models.CharField(max_length=50,primary_key=True)
    nombre=models.CharField(blank=False,max_length=40)

class Pedido(models.Model):
    empleado=models.ForeignKey(Empleado,on_delete=models.CASCADE,primary_key=True)
    calendario=models.ForeignKey(Calendario,on_delete=models.CASCADE)
    fechaHora=models.DateTimeField()
    customizacion=models.CharField(blank=True,max_length=20)
    menu=models.ForeignKey(Menu,on_delete=models.CASCADE)
    def __str__(self):
        return '%s////%s///%s' % (self.menu,self.customizacion,self.fechaHora)

    class Meta:
        unique_together = (('empleado', 'calendario'),)





