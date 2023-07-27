from flask import Flask,request,Response,render_template,redirect,url_for, session
from http import HTTPStatus
import funciones.funciones
import secrets
import json

app = Flask(__name__)
app.secret_key = 's94LQfKH83jxfr7o0ZQDfdttRznMeX4rZR0Q3sU8otma8WNYCuTWBViUosLhepjA'

@app.route("/")
def retornar():
  return redirect(url_for("index"),Response=HTTPStatus.OK)

@app.route("/peliculas",methods=["GET"])
def index():
  return Response (render_template("peliculas.html", user=funciones.funciones.verify(), 
  nombre_peliculas=funciones.funciones.nombresPeliculas(), 
  imagenes_peliculas=funciones.funciones.imgPeliculas()), status = HTTPStatus.OK)

@app.route("/buscar/<int:info>",methods=["GET"])
@app.route("/buscar/<info>",methods=["GET"])
def buscar(info):
    lista_encontradas=[]
    peliculas = funciones.funciones.moviesFiles()
    for i in peliculas[::-1]:
        for j in i.values():
            if str(info).isnumeric():
                if ((str(info) in str(j)) and (i not in lista_encontradas)) and (len(lista_encontradas)<10):
                    lista_encontradas.append(i)
            else:
                if ((info in str(j)) and (i not in lista_encontradas)) and (len(lista_encontradas)<10):
                      lista_encontradas.append(i)

    return Response (render_template("peliculas.html",
      nombre_peliculas=[i["Nombre"] for i in lista_encontradas],
      imagenes_peliculas=[i["img"] for i in lista_encontradas]),
      status = HTTPStatus.OK)

@app.route("/buscar", methods=["POST"])
def buscar_post():
    informacion=request.form["info_buscar"]

    return redirect(url_for("buscar", info=informacion, next="edit"), Response=HTTPStatus.OK) 

@app.route("/dgi")
def dGI():
  return Response (render_template("dirandgen.html", 
  user=funciones.funciones.verify(),directores=funciones.funciones.Directores,
  generos=funciones.funciones.Generos, imagenes=funciones.funciones.pelisConImg()),status=HTTPStatus.OK)

@app.route('/login', methods=['GET', 'POST'])
@app.route('/perfil', methods=['GET', 'POST'])
def login():
  if 'username' in session:
    return redirect(url_for('index'))
  if request.method == 'POST':
    dataUser = {
      "username": request.form['username'],
      "password": request.form['password']
    }
    users = funciones.funciones.usersFiles()
    for user in users:
      if dataUser["username"] == user["Usuario"] and dataUser["password"] == user["Contrasenia"]:
        session["username"] = dataUser['username']
        user = dataUser['username']
      else:
        user = ""
    return Response (render_template("peliculas.html", user=user, 
    nombre_peliculas=funciones.funciones.nombresPeliculas(), 
    imagenes_peliculas=funciones.funciones.imgPeliculas()), status = HTTPStatus.OK)
  return render_template('perfil.html', user=funciones.funciones.verify())


@app.route('/logout')
def logout():
  session.pop('username', None)
  return redirect(url_for('index'))

@app.route('/pelicula/<nombrePelicula>')
def pelicula(nombrePelicula):
  pelis = funciones.funciones.moviesFiles()
  for peli in pelis:
    if peli["Nombre"] == nombrePelicula:
      unaPeli = peli
      return render_template('comentarios.html', unaPeli=unaPeli, 
      user=funciones.funciones.verify(), comentarios=funciones.funciones.siHayComentarios(nombrePelicula))
  
@app.route('/pelicula/agregar', methods=['GET', 'POST'])
def agregarPelicula():
  if request.method == 'POST':
    pelicula = {
        "id":secrets.token_hex(),
        "Nombre":request.form['nombre'],
        "Anio":request.form['anio'],
        "Fecha_Estreno":request.form['estreno'],
        "Director":request.form['director'],
        "Genero":request.form['genero'],
        "img":request.form['imagen'],
        "Comentarios":[
          {
            "idComent":secrets.token_hex(),
            "opinion":request.form['opinion']
          }
        ],
        "sinopsis":request.form['sinopsis']
    }
    funciones.funciones.agregarPeliculas(pelicula, session['username'])
  return render_template('add_pelicula.html', directores=funciones.funciones.Directores, generos=funciones.funciones.Generos)

@app.route('/pelicula/eliminar/<peli>', methods=["GET","POST"])
def eliminarPeli(peli):
  if request.method == "POST":
    funciones.funciones.eliminarPeli(peli)
    return redirect(url_for('index'))
  return render_template('del_pelicula.html', peli=peli, user=funciones.funciones.verify())

@app.route("/pelicula/editar/<peli>",methods=["GET","POST"])
def editarPeli(peli):
  pelicula_mod_id=funciones.funciones.retPeli(peli)["id"]
  if request.method=="POST":
    peliculaEdicion = {
      "Id":pelicula_mod_id,
      "Nombre":request.form['Nombre'],
      "Anio":request.form['Anio'],
      "Fecha_Estreno":request.form['estreno'],
      "Director":request.form['Director'],
      "Genero":request.form['Genero'],
      "img":request.form['imagen'],
      "Sinopsis":request.form['Sinopsis']
    }
    funciones.funciones.update(peliculaEdicion)
    return redirect(url_for('index'))
  return render_template("editarPeli.html", pelicula_encontrada=funciones.funciones.retornarPeli(peli))

@app.route('/all')
def allPelis():
  peliculas = funciones.funciones.moviesFiles()
  return Response (render_template("all.html", user=funciones.funciones.verify(), all=peliculas), status = HTTPStatus.OK)

if __name__ == "__main__":
  app.run(debug=True)