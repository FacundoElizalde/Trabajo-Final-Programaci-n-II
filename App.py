from flask import Flask,request, jsonify, Response,render_template,redirect,url_for, session
from http import HTTPStatus
import funciones.funciones
import secrets

app = Flask(__name__)
app.secret_key = 's94LQfKH83jxfr7o0ZQDfdttRznMeX4rZR0Q3sU8otma8WNYCuTWBViUosLhepjA'

@app.route("/")
def retornar():
  return redirect(url_for("index"),Response=HTTPStatus.OK)

@app.route("/home",methods=["GET"])
def index():
  return Response (render_template("peliculas.html", user=funciones.funciones.verify(), 
  nombre_peliculas=funciones.funciones.names_movies(), 
  imagenes_peliculas=funciones.funciones.img_movies()), status = HTTPStatus.OK)

@app.route("/buscar/<int:info>",methods=["GET"])
@app.route("/buscar/<info>",methods=["GET"])
def buscar(info):
    lista_encontradas=[]
    peliculas = funciones.funciones.movies_files()
    for i in peliculas[::-1]:

        for j in i.values():
            if str(info).isnumeric():
                if ((str(info) in str(j)) and (i not in lista_encontradas)) and (len(lista_encontradas)<10):
                    lista_encontradas.append(i)
            else:
                if ((info.lower() in str(j).lower()) and (i not in lista_encontradas)) and (len(lista_encontradas)<10):
                      lista_encontradas.append(i)

    return Response (render_template("peliculas.html",
      nombre_peliculas=[i["Nombre"] for i in lista_encontradas],
      imagenes_peliculas=[i["img"] for i in lista_encontradas],
      user=funciones.funciones.verify()),
      status = HTTPStatus.OK)

@app.route("/buscar", methods=["POST"])
def buscar_post():
    informacion=request.form["info_buscar"]
    return redirect(url_for("buscar", info=informacion, next="edit"), Response=HTTPStatus.OK) 

@app.route("/infoadicional")
def dGI():
  return Response (render_template("info_adicional.html", 
  user=funciones.funciones.verify(),directores = funciones.funciones.Directores,
  generos=funciones.funciones.Generos, imagenes = funciones.funciones.movies_w_img()),status=HTTPStatus.OK)

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
    users = funciones.funciones.user_files()
    for user in users:
      if dataUser["username"] == user["Usuario"] and dataUser["password"] == user["Contrasenia"]:
        session["username"] = dataUser['username']
        user = dataUser['username']
      else:
        user = ""
    return Response (render_template("peliculas.html", user=user, 
    nombre_peliculas=funciones.funciones.names_movies(), 
    imagenes_peliculas=funciones.funciones.img_movies()), status = HTTPStatus.OK)
  return render_template('perfil.html', user=funciones.funciones.verify())

@app.route('/logout')
def logout():
  session.pop('username', None)
  return redirect(url_for('index'))
  
@app.route('/pelicula/<nombre_pelicula>', methods=['GET', 'POST'])
def pelicula(nombre_pelicula):
  if request.method == "POST":
    coment = {
      "usuario":session["username"],
      "comentario":request.form["comentario"]
    }
    funciones.funciones.comentar(coment, nombre_pelicula)
    return redirect(url_for('index'))
  pelis = funciones.funciones.movies_files()
  for peli in pelis:
    if peli["Nombre"] == nombre_pelicula:
      return render_template('comentarios.html', 
      unaPeli=peli,
      user=funciones.funciones.verify(),
      comentarios=funciones.funciones.if_coments(nombre_pelicula),
      )
  
@app.route('/pelicula/add', methods=['GET', 'POST'])
def agregarPelicula():
  if 'username' not in session:
    return redirect(url_for('index'))
  if request.method == 'POST':
    pelicula = {
        "Id":secrets.token_hex(),
        "Nombre":request.form['nombre'],
        "Anio":request.form['anio'],
        "Fecha_Estreno":request.form['estreno'],
        "Director":request.form['director'],
        "Genero":request.form['genero'],
        "img":request.form['imagen'],
        "Comentarios":[
          {
            "usuario":session["username"],
            "comentario":request.form['opinion']
          }
        ],
        "Sinopsis":request.form['sinopsis']
    }
    funciones.funciones.add_movies(pelicula, session['username'])
  return render_template('add_pelicula.html', directores=funciones.funciones.Directores, generos=funciones.funciones.Generos)

@app.route('/pelicula/eliminar/<peli>', methods=["GET","POST"])
def del_pelicula(peli):
  if 'username' not in session:
    return redirect(url_for('index'))
  else:
    if request.method == "POST":
      funciones.funciones.del_pelicula(peli)
      return redirect(url_for('index'))
    return render_template('del_pelicula.html', peli=peli, user=funciones.funciones.verify())

@app.route("/pelicula/editar/<peli>",methods=["GET", "POST"])
def edit_pelicula(peli):
  if 'username' not in session:
    return redirect(url_for('index'))
  else:
    pelicula_mod_id=funciones.funciones.ret_movie(peli)["Id"]
    if request.method=="POST":
      peliculaEdicion = {
        "Id":pelicula_mod_id,
        "Nombre":request.form['nombre'],
        "Anio":request.form['anio'],
        "Fecha_Estreno":request.form['estreno'],
        "Director":request.form['director'],
        "Genero":request.form['genero'],
        "img":request.form['imagen'],
        "Sinopsis":request.form['sinopsis']
      }
      funciones.funciones.update(peliculaEdicion)
      return redirect(url_for('index'))
    return render_template("edit_pelicula.html", pelicula_encontrada = funciones.funciones.ret_movie(peli), 
    directores=funciones.funciones.Directores, generos=funciones.funciones.Generos)

@app.route('/allmovies')
def allPelis():
  peliculas = funciones.funciones.movies_files()
  return Response (render_template("all.html", 
  user=funciones.funciones.verify(), all=peliculas), 
  status = HTTPStatus.OK)

@app.route('/directores', methods=["GET"])
def obtenerDirectores():
    return jsonify({"Directores presentes en la plataforma": funciones.funciones.Directores})

@app.route('/agregar/agregar_director', methods=['POST'])
def agregarDirector():
    nuevo_director = request.json.get('nuevo_director')

    if nuevo_director:
        if nuevo_director not in funciones.funciones.Directores:
            funciones.funciones.Directores.append(nuevo_director)
            return jsonify({"mensaje": "Director agregado exitosamente"})
        else:
            return jsonify({"mensaje": "El director ya existe en la lista"})
    else:
      return jsonify({"mensaje": "Error al agregar el director"})


@app.route('/generos', methods=['GET'])
def getGeneros():
    return jsonify({"Generos presentes en la plataforma": funciones.funciones.Generos})

@app.route('/agregar/agregar_genero', methods=['POST'])
def agregarGenero():
    nuevo_genero = request.json.get('nuevo_genero')

    if nuevo_genero:
        if nuevo_genero not in funciones.funciones.Generos:
            funciones.funciones.Generos.append(nuevo_genero)
            return jsonify({"mensaje": "Genero agregado exitosamente"})
        else:
            return jsonify({"mensaje": "El genero ya existe en la lista"})
    else:
        return jsonify({"mensaje": "Error al agregar el genero"})


@app.route('/<director>', methods=['GET'])
def peliculaDirigida(director):
    pelis = funciones.funciones.movies_files()
    peliculas_dirigidas = []

    for peli in pelis:
        if peli["Director"] == director:
            peliculas_dirigidas.append(peli["Nombre"])
    
    return jsonify({"Peliculas en el sitio dirigidas por " + director: peliculas_dirigidas})

@app.route('/peliculas_con_imagen', methods=['GET'])
def peliculasConImagen():
    pelis = funciones.funciones.movies_files()
    
    peliculas_con_imagen = []

    for peli in pelis:
        if peli.get("img"):
            peliculas_con_imagen.append(peli["Nombre"])
    
    return jsonify({"Peliculas con imagen": peliculas_con_imagen})

if __name__ == "__main__":
  app.run(debug=True)

