from django.db import models  # hereda del modelo base de django
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    organizacion = models.TextField(max_length=30, default="Ninguna")
    email = models.EmailField(blank=False)

    def __str__(self):  # version imprimible
        return self.usuario.username


def crear_usuario_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(usuario=instance)


def guardar_usuario_perfil(sender, instance, **kwargs):
    instance.pefil.save()


class Categoria(models.Model):
    categoria = models.CharField(max_length=20)
    descripcion = models.TextField()


class Noticia(models.Model):
    id_noticia = models.IntegerField(primary_key=True)
    titulo = models.TextField()
    descripcion = models.TextField()
    url = models.TextField()
    urlImagen = models.TextField()
    fecha = models.DateTimeField()
    autor = models.CharField(max_length=50)
    nombre = models.CharField(max_length=50)


class Preferencia(models.Model):
    id_noticia = models.IntegerField()
    usuario = models.CharField(max_length=50)
    preferencia = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id_noticia)


class Fuente(models.Model):
    CATEGORIAS = (
        ('P', 'Politica'),
        ('S', 'Salud'),
        ('E', 'Econpmia'),
    )
    diario = models.CharField(max_length=50)
    url = models.TextField(max_length=250)
    categoria = models.CharField(max_length=1, choices=CATEGORIAS)
    activo = models.BooleanField(default=False)


# el modelo se debe instalar en settings.py
# luego hacer las migraciones
# python manage.py makemigration
# python manage.py migrate
