import requests
import pprint
import random
import feedparser
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, forms
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from .models import Curso
# Create your views here.

app_name = "main"

Mensaje = "holaaaaaaa"


secret = "5f039f3f100a42cdbc4aa9661082475f"

# Define the endpoint
url = 'http://newsapi.org/v2/everything?'

# Specify the query and
# number of returns
parameters = {
    'q': 'rebrote',  # query phrase
    'pageSize': 100,  # maximum is 100
    'apiKey': secret,  # your own API key
    'language': 'es',

}

# Make the request
response = requests.get(url,
                        params=parameters)

# Convert the response to
# JSON format and pretty print it
response_json = response.json()


class articulo:
    def __init__(self, article):
        self.titulo = article['title']
        self.descripcion = article['description']
        self.url = article['url']
        self.urlImagen = article['urlToImage']
        self.fecha = article['publishedAt']
        self.autor = article['author']
        self.nombre = article['source']['name']


def extraerArticulosAPI(response_json):
    for a in response_json['articles']:
        yield(articulo(a))


articulos1 = list(extraerArticulosAPI(response_json))


feedsPolitica = [
    {'diario': 'El Comercio',
        'urlfeed': "https://elcomercio.pe/arcio/rss/category/politica/"},
    {'diario': 'La República',
        'urlfeed': "https://larepublica.pe/rss/politica.xml?outputType=rss"},
    {'diario': 'Peru.com',
        'urlfeed': "https://peru.com/feed/actualidad/politicas"},
    {'diario': 'Diario Correo',
        'urlfeed': "https://diariocorreo.pe/arcio/rss/category/politica/?ref=dcr"},
    # {'diario': 'El Perfil',
    #     'urlfeed': "https://elperfil.pe/politica/feed/"},
]

feedsSalud = [
    {'diario': 'Peru.com',
        'urlfeed': "https://peru.com/feed/estilo-de-vida/salud"},
    {'diario': 'Diario Correo',
        'urlfeed': "https://diariocorreo.pe/arcio/rss/category/salud/?ref=dcr"},
    {'diario': 'La República',
        'urlfeed': "https://larepublica.pe/rss/salud.xml?outputType=rss"},
    # {'diario': 'El Perfil',
    #     'urlfeed': "https://elperfil.pe/salud/feed/"},
]

feedsEconomia = [
    {'diario': 'Peru.com',
        'urlfeed': "https://peru.com/feed/actualidad/economia-y-finanzas"},
    {'diario': 'Diario Correo',
        'urlfeed': "https://diariocorreo.pe/arcio/rss/category/economia/?ref=dcr"},
    {'diario': 'La República',
        'urlfeed': "https://larepublica.pe/rss/economia.xml?outputType=rss"},
    # {'diario': 'El Perfil',
    #     'urlfeed': "https://elperfil.pe/economia/feed/"},
    {'diario': 'El Comercio',
        'urlfeed': "https://elcomercio.pe/arcio/rss/category/economia/"},
]

# feedsAgricultura = [
#     http://www.fao.org/americas/noticias/rss/feed/es /?key= 33
#     https://elperfil.pe/actualidad/feed /

# ]


def extraerArticulos(feeds):
    for feed in feeds:
        rss = feedparser.parse(feed['urlfeed'])
        for item in rss['entries']:
            article = dict()
            article['title'] = item['title']
            article['description'] = item['summary']
            article['url'] = item['link']
            article['urlToImage'] = '#'
            article['publishedAt'] = item['published']
            article['author'] = ''
            article['source'] = dict()
            article['source']['name'] = feed['diario']
            yield articulo(article)


articulosPolitica = list(extraerArticulos(feedsPolitica))
articulosSalud = list(extraerArticulos(feedsSalud))
articulosEconomia = list(extraerArticulos(feedsEconomia))
articulos = articulosPolitica + articulosSalud + articulosEconomia

categorias = [
    {'nomcat': 'politica', 'textcat': 'Política'},
    {'nomcat': 'economia', 'textcat': 'Economía'},
    {'nomcat': 'salud', 'textcat': 'Salud'},
]


def homepage(request):
    # recibe dato, nomplantilla y diccionario de variables(opcional)
    random.shuffle(articulos)
    return render(request, "main/inicio.html", {"news": articulos, "activa": "todos", "categorias": categorias, })
    # return HttpResponse("Hola mundo") #por ahora retorna una http


def politica(request):
    random.shuffle(articulosPolitica)
    return render(request, "main/inicio.html", {"news": articulosPolitica, "categoria": "politica", "activa": "politica", "categorias": categorias, })


def economia(request):
    random.shuffle(articulosEconomia)
    return render(request, "main/inicio.html", {"news": articulosEconomia, "categoria": "economia", "activa": "economia", "categorias": categorias, })


def salud(request):
    random.shuffle(articulosSalud)
    return render(request, "main/inicio.html", {"news": articulosSalud, "categoria": "salud", "activa": "salud", "categorias": categorias, })


def registro(request):
    form = UserCreationForm()
    forms.CharField
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            usuario = form.save()
            nombre_usuario = form.cleaned_data.get(
                'username')  # obtiene el nombre del usuario
            # crea un mensaje para el usuario
            messages.success(
                request, f"Nueva Cuenta Creada : {nombre_usuario}")
            login(request, usuario)
            messages.info(request, f"Has sido logueado como {nombre_usuario}")
            return redirect("main:homepage")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

    return render(request, "main/registro.html", {"form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "Saliste exitosamente")
    return redirect("main:homepage")


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.cleaned_data.get('username')
            contraseña = form.cleaned_data.get('password')
            user = authenticate(username=usuario, password=contraseña)

            if user is not None:
                login(request, user)
                messages.info(request, f"Estas logueado como {usuario}")
                return redirect("main:homepage")
            else:
                messages.error(request, "Usuario o contraseña equivoacada")
        else:
            messages.error(request, "Usuario o contraseña equivoacada")

    form = AuthenticationForm()
    return render(request, "main/login.html", {"form": form})
