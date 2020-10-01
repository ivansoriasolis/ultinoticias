from django.contrib import admin
# se debe registrar el modelo para que aparezca en el administrador
from .models import Preferencia, Noticia
from tinymce.widgets import TinyMCE  # importa el plugin tinymce
from django.db import models  # es necesario importar para poder haceerle un override

# Register your models here.


class PreferenciaAdmin(admin.ModelAdmin):
    list_display = ("id_noticia",
                    "usuario",
                    )


class NoticiaAdmin(admin.ModelAdmin):
    list_display = ("id_noticia",
                    "titulo",
                    "descripcion",
                    "url",
                    "urlImagen",
                    "fecha",
                    "autor",
                    "nombre",
                    )


admin.site.register(Preferencia, PreferenciaAdmin)
admin.site.register(Noticia, NoticiaAdmin)

# esto resitra el modelo django le agregara una s al nombre del modelo
