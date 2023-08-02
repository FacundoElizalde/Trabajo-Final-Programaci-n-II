from flask import session
import json

Generos = ["Comedia", "Drama", "Romance", "Ciencia Ficcion", "Accion", "Terror", "Western", "Documental", "Musical", "Thriller", 
           "Epico", "Belico", "Deportes", "Animacion", "Crimen"]

Directores = ["Louis Leterrier", "Greta Gerwig", "Christoper Nolan", "Francis Ford Coppola", "Jaume Collet-Serra", "Jung Su-yee",
             "Steven Caple Jr.", "Stanley Kubrick", "Robert Zemeckis", "James Mangold", "Martin Scorsese", "Quentin Tarantino",
             "Woody Allen", "Juan Jose Campanella", "Carlos Saldanha", "John Lasseter", "Santiago Mitre", "Justin Lin"]

def movies_files():
  with open('./json/peliculas.json', encoding='utf-8') as archivo_json1:
    peliculas = json.load(archivo_json1)
  return peliculas

def user_files():
  with open('./json/usuarios.json', encoding='utf-8') as archivo_json1:
    users = json.load(archivo_json1)
  return users

def names_movies():
  nombres = []
  peliculas = movies_files()
  for i in peliculas[::-1]:
    if (len(nombres)<10) and (i["Nombre"] not in nombres):
        nombres.append(i["Nombre"])
  return nombres

def img_movies(): 
  img = []
  peliculas = movies_files()
  for i in peliculas[::-1]:
    if (len(img)<10) and (i["img"] not in img):
      img.append(i["img"])
  return img

def add_movies(pelicula, userSession):
  movies = movies_files()
  movies.append(pelicula)
  with open('./json/peliculas.json', 'w') as f:
    json.dump(movies, f, indent=4)
    f.close()
  users = user_files()
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

def movies_w_img():
  imagenes=[]
  for i in movies_files():
    if i["img"]!="":
      imagenes.append(i["Nombre"])
  return imagenes

def ret_movie(peli):
    for i in movies_files():
        if i["Nombre"] == peli:
            return i

def if_coments(nombrePeli):
  movies = movies_files()
  for movie in movies:
    if movie['Nombre'] == nombrePeli:
      if len(movie['Comentarios']) >= 1:
        return 1
      else:
        return 2

def comentar(comentario, pelicula):
  movies = movies_files()
  users = user_files()
  id = ret_movie(pelicula)["Id"]
  for movie in movies:
    if movie["Nombre"] == pelicula:
      movie["Comentarios"].append(comentario)
  for user in users:
    if user["Usuario"] == comentario["usuario"]:
      user["Peliculas_Comentadas"].append(id)
  with open('./json/usuarios.json', 'w') as f:
    json.dump(users, f, indent=4)
    f.close()
  with open('./json/peliculas.json', 'w') as f:
    json.dump(movies, f, indent=4)
    f.close()

def update(peli):
  dataMovies = movies_files()
  for movie in dataMovies:
    if movie["Id"] == peli["Id"]:
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

def del_pelicula(peli):
  movies = movies_files()
  for movie in movies:
    if movie['nombre'] == peli:
      movies.remove(movie)
  with open('./json/peliculas.json', 'w') as f:
    json.dump(movies, f, indent=4)
    f.close()