from django.db import models
from django.contrib.auth.models import AbstractUser

class Animal(models.Model):
    sexo = models.CharField(max_length=100)
    edad = models.IntegerField()
    descripcion = models.TextField(max_length=200)
    estado_salud = models.TextField(max_length=300)
    class Meta:
        app_label = 'App'

class Perro(Animal):
    raza = models.CharField(max_length=100)
    

class Gato(Animal):
    color_pelo = models.CharField(max_length=100)



class Usuario(AbstractUser):
    nombre_usuario = models.CharField(max_length=100)
    contraseña = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_usuario

    def verificar_credenciales(self, nombre_usuario, contraseña):
        return self.nombre_usuario == nombre_usuario and self.contraseña == contraseña

# Añadir este campo para especificar un related_name único para groups
Usuario.groups.field.remote_field.related_name = 'usuario_groups'

# Añadir este campo para especificar un related_name único para user_permissions
Usuario.user_permissions.field.remote_field.related_name = 'usuario_permissions'