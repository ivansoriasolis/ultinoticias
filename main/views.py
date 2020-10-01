from time import mktime
from datetime import datetime
import unicodedata
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import requests
import pprint
import random
import feedparser
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, forms
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
import hashlib

from .models import Preferencia, Noticia
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
        h = hashlib.md5()
        h.update(article['title'].encode('utf-8'))
        self.id = int(h.hexdigest(), 16) % 10000000
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
            article['publishedAt'] = datetime.strptime(
                item['published'][5:25], '%d %b %Y %H:%M:%S')
            article['author'] = ''
            article['source'] = dict()
            article['source']['name'] = feed['diario']
            yield articulo(article)


articulosPolitica = list(extraerArticulos(feedsPolitica))
articulosSalud = list(extraerArticulos(feedsSalud))
articulosEconomia = list(extraerArticulos(feedsEconomia))
articulos = articulosPolitica + articulosSalud + articulosEconomia

# for articulo in articulos:
#     consulta = Noticia.objects.filter(id_noticia=articulo.id)
#     instancia = None
#     if consulta.count() == 0:
#         instancia = Noticia.objects.create(
#             id_noticia=articulo.id,
#             titulo=articulo.titulo,
#             descripcion=articulo.descripcion,
#             url=articulo.url,
#             urlImagen=articulo.urlImagen,
#             fecha=articulo.fecha,
#             autor=articulo.autor,
#             nombre=articulo.nombre,
#         )
#     else:
#         instancia = consulta[0]
#     instancia.save()


articulosPolitica.sort(key=lambda x: x.fecha, reverse=True)
articulosSalud.sort(key=lambda x: x.fecha, reverse=True)
articulosEconomia.sort(key=lambda x: x.fecha, reverse=True)
articulos.sort(key=lambda x: x.fecha, reverse=True)

f = open("datos.csv", "w", encoding="utf-8")
f.write('id,description\n')
for articulo in articulos:
    linea = "" + str(articulo.id) + ",\"" + articulo.titulo + \
        "-" + articulo.descripcion + "\"\n"
    f.write(linea)
f.close()


def normalizatexto(texto):
    return unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').strip().lower()





categorias = [
    {'nomcat': 'politica', 'textcat': 'Política'},
    {'nomcat': 'economia', 'textcat': 'Economía'},
    {'nomcat': 'salud', 'textcat': 'Salud'},
    # {'nomcat': 'recomendados', 'textcat': 'Recomendados para ti'},
]


ds = pd.read_csv("datos.csv", usecols=["id", "description"], encoding="latin")

tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3),
                     min_df=0, stop_words='english')
tfidf_matrix = tf.fit_transform(ds['description'])

cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

results = {}

for idx, row in ds.iterrows():
    similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
    similar_items = [(cosine_similarities[idx][i], ds['id'][i])
                     for i in similar_indices]

    results[row['id']] = similar_items[1:]


def item(id):
    return ds.loc[ds['id'] == id]['description'].tolist()[0].split(' - ')[0]


def recommend(item_id, num):
    recs = results[item_id][:num]
    return recs


def homepage(request):
    # recibe dato, nomplantilla y diccionario de variables(opcional)
    # random.shuffle(articulos)
    # usuario_actual = request.user
    # consultaPreferencias = Preferencia.objects.filter(
    #     usuario=usuario_actual)
    # preferencias = [
    #     preferencia.id_noticia for preferencia in consultaPreferencias]
    # print("PREFERENCIAS", preferencias)
    # print("ARTICULO", articulos[0].id)
    # return render(request, "main/inicio.html", {"news": articulos, "activa": "recomendados", "categorias": categorias, "preferencias": preferencias, })
    # return HttpResponse("Hola mundo") #por ahora retorna una http
    return HttpResponse('')


def politica(request):
    # random.shuffle(articulosPolitica)
    usuario_actual = request.user
    consultaPreferencias = Preferencia.objects.filter(
        usuario=usuario_actual)
    preferencias = [
        preferencia.id_noticia for preferencia in consultaPreferencias]
    return render(request, "main/inicio.html", {"news": articulosPolitica, "categoria": "politica", "activa": "politica", "categorias": categorias, "preferencias": preferencias, })


def economia(request):
    # random.shuffle(articulosEconomia)
    usuario_actual = request.user
    consultaPreferencias = Preferencia.objects.filter(
        usuario=usuario_actual)
    preferencias = [
        preferencia.id_noticia for preferencia in consultaPreferencias]
    return render(request, "main/inicio.html", {"news": articulosEconomia, "categoria": "economia", "activa": "economia", "categorias": categorias, "preferencias": preferencias, })


def salud(request):
    # random.shuffle(articulosSalud)
    usuario_actual = request.user
    consultaPreferencias = Preferencia.objects.filter(
        usuario=usuario_actual)
    preferencias = [
        preferencia.id_noticia for preferencia in consultaPreferencias]
    return render(request, "main/inicio.html", {"news": articulosSalud, "categoria": "salud", "activa": "salud", "categorias": categorias, "preferencias": preferencias, })


def busqueda(request):
    usuario_actual = request.user
    consultaPreferencias = Preferencia.objects.filter(
        usuario=usuario_actual)
    preferencias = [
        preferencia.id_noticia for preferencia in consultaPreferencias]
    textobuscado = normalizatexto(request.GET['search'])
    articulosBusqueda = [
        articulo for articulo in articulos if textobuscado in normalizatexto(articulo.titulo)]
    return render(request, "main/inicio.html", {"news": articulosBusqueda, "categoria": "Busqueda", "activa": "Busqueda", "categorias": categorias, "preferencias": preferencias, })


def recomendados(request):
    usuario_actual = request.user
    consultaPreferencias = Preferencia.objects.filter(
        usuario=usuario_actual)
    preferencias = [
        preferencia.id_noticia for preferencia in consultaPreferencias]
    elegido = random.randint(0, len(articulos))
    id_elegido = articulos[elegido].id
    recomendaciones = recommend(item_id=id_elegido, num=10)
    ids_recomendados = [item[1] for item in recomendaciones]
    articulosrecomendados = [
        articulo for articulo in articulos if articulo.id in ids_recomendados and not articulo.id in preferencias]
    # print("PREFERENCIAS", preferencias)
    # print("ARTICULO", articulosrecomendados)
    return render(request, "main/inicio.html", {"news": articulosrecomendados, "categoria": "recomendados", "activa": "recomendados", "categorias": categorias, })


def check(request):
    noticia = request.GET['id']
    check = request.GET['click']
    usuario = request.GET['usuario']
    consulta = Preferencia.objects.filter(
        usuario=request.user).filter(id_noticia=noticia)
    if (len(consulta) == 0):
        nuevocheck = Preferencia.objects.create(
            id_noticia=noticia, preferencia=True, usuario=usuario)
        nuevocheck.save()
        return HttpResponse('true')
    consulta.delete()
    return HttpResponse('false')


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
