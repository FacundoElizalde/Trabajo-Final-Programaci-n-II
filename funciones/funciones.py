import json

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