from django.db import models  # hereda del modelo base de django
from datetime import datetime

# Create your models here.


class Curso(models.Model):
    curso_titulo = models.CharField(max_length=200)
    curso_contenido = models.TextField()
    curso_publicado = models.DateTimeField(
        "Fecha de publicacion", default=datetime.now())  # la hora y fecha actual por defecto

    def __str__(self):
        return self.curso_titulo


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
