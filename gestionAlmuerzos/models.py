from django.db import models

# Creacion de todos mis modelos

# Modelo de Menu
class Menu(models.Model): 
    #menu_id=models.IntegerField(primary_key=True)
    plato_fuerte=models.CharField(blank=False,max_length=30)
    ensalada=models.CharField(blank=True,max_length=30)
    postre=models.CharField(blank=True,max_length=30)
    #nora=models.ForeignKey(Nora,on_delete=models.CASCADE, null=True)
    def __str__(self):
        return '%s-%s-%s' % (self.plato_fuerte,self.ensalada,self.postre)

# Modelo de Calendario, pordria ser importante, ya que se pueden dejar notas diarias
class Calendario(models.Model):
    fecha=models.DateField(primary_key=True)
    descripcion=models.TextField(blank=True)

# Modelo de Empleado
class Empleado(models.Model):
    uuid=models.CharField(max_length=50,primary_key=True)
    nombre=models.CharField(blank=False,max_length=40)
    def __str__(self):
        return '%s' % (self.nombre)

# Modelo de Pedido
class Pedido(models.Model):
    empleado=models.ForeignKey(Empleado,on_delete=models.CASCADE,primary_key=True)
    calendario=models.ForeignKey(Calendario,on_delete=models.CASCADE)
    fechaHora=models.DateTimeField()
    customizacion=models.CharField(blank=True,max_length=100)
    menu=models.ForeignKey(Menu,on_delete=models.CASCADE)
    def __str__(self):
        return 'Empleado: %s, Menu: %s, Customizacion: %s, Fecha: %s' % (self.empleado,self.menu,self.customizacion,self.fechaHora)

    class Meta:
        unique_together = (('empleado', 'calendario'),)





