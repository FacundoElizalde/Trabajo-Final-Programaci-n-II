import json
from flask import session

Generos = ["Comedia", "Drama", "Romance", "Ciencia Ficcion", "Accion", "Terror", "Western", "Documental", "Musical", "Thriller", "Epico", "Belico"]
Directores = ["Louis Leterrier", "Greta Gerwig", "Christoper Nolan", "Francis Ford Coppola", "Jaume Collet-Serra", "Jung Su-yee",
             "Steven Caple Jr.", "Stanley Kubrick", "Robert Zemeckis"]


def moviesFiles():
  with open('./json/peliculas.json', encoding='utf-8') as archivo_json1:
    peliculas = json.load(archivo_json1)
  return peliculas

def usersFiles():
  with open('./json/usuarios.json', encoding='utf-8') as archivo_json1:
    users = json.load(archivo_json1)
  return users

def nombresPeliculas():
  nombres = []
  peliculas = moviesFiles()
  for i in peliculas[::-1]:
    if (len(nombres)<10) and (i["Nombre"] not in nombres):
        nombres.append(i["Nombre"])
  return nombres

def imgPeliculas(): 
  img = []
  peliculas = moviesFiles()
  for i in peliculas[::-1]:
    if (len(img)<10) and (i["img"] not in img):
      img.append(i["img"])
  return img

def agregarPeliculas(pelicula, userSession):
  movies = moviesFiles()
  movies.append(pelicula)
  with open('./json/peliculas.json', 'w') as f:
    json.dump(movies, f, indent=4)
    f.close()
  for idCom in pelicula['Comentarios']:
    idComentario = idCom['idComent']
  users = usersFiles()
  for user in users:
    if userSession == user['Usuario']:
      user['peliculas_comentadas'] = [{
        "idPeli":pelicula['id'],
        "idComentario":idComentario
      }]
  with open('./json/usuarios.json', 'w') as f:
    json.dump(users, f, indent=4)
    f.close()

def verify():
  if 'username' in session:
    user = session['username']
  else:
    user = ""
  return user

def pelisConImg():
  imagenes=[]
  for i in moviesFiles():
    if i["img"]!="":
      imagenes.append(i["Nombre"])
  return imagenes