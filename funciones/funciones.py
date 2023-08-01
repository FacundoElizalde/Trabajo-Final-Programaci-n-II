import json
from flask import session

Generos = ["Comedia", "Drama", "Romance", "Ciencia Ficcion", "Accion", "Terror", "Western", "Documental", "Musical", "Thriller", 
           "Epico", "Belico", "Deportes", "Animacion"]
Directores = ["Louis Leterrier", "Greta Gerwig", "Christoper Nolan", "Francis Ford Coppola", "Jaume Collet-Serra", "Jung Su-yee",
             "Steven Caple Jr.", "Stanley Kubrick", "Robert Zemeckis", "James Mangold", "Martin Scorsese", "Quentin Tarantino",
             "Woody Allen", "Juan Jose Campanella", "Carlos Saldanha"]


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
  users = usersFiles()
  for user in users:
    if userSession == user['Usuario']:
      user['Peliculas_Comentadas'].append(pelicula['Id'])
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

def retPeli(peli):
    for i in moviesFiles():
        if i["Nombre"] == peli:
            return i

def siHayComentarios(nombrePeli):
  movies = moviesFiles()
  for movie in movies:
    if movie['Nombre'] == nombrePeli:
      if len(movie['Comentarios']) > 0:
        return 1
      else:
        return 2

def hacerComentario(comentario, pelicula):
  movies = moviesFiles()
  users = usersFiles()
  id = retPeli(pelicula)["Id"]
  for movie in movies:
    if movie["Nombre"] == pelicula:
      movie["Comentarios"].append(comentario)
  for user in users:
    if user["Usuario"] == comentario["usuario"]:
      user["peliculas_comentadas"].append(id)
  with open('./json/usuarios.json', 'w') as f:
    json.dump(users, f, indent=4)
    f.close()
  with open('./json/peliculas.json', 'w') as f:
    json.dump(movies, f, indent=4)
    f.close()

def del_pelicula(peli):
  movies = moviesFiles()
  for movie in movies:
    if movie['nombre'] == peli:
      movies.remove(movie)
  with open('./json/peliculas.json', 'w') as f:
    json.dump(movies, f, indent=4)
    f.close()

def update(peli):
  dataMovies = moviesFiles()
  for movie in dataMovies:
    if peli["Id"] == movie["Id"]:
      movie["Nombre"] = peli["Nombre"]
      movie["Anio"] = peli["Anio"]
      movie["Fecha_Estreno"] = peli["Fecha_Estreno"]
      movie["img"] = peli["img"]
      movie["Director"] = peli["Director"]
      movie["Genero"] = peli["Genero"]
      movie["Sinopsis"] = peli["Sinopsis"]
  with open('./json/peliculas.json', "w") as file:
   json.dump(dataMovies, file, indent=4)
   file.close()
