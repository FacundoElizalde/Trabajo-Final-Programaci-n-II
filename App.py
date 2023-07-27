from flask import Flask,request,Response,render_template,redirect,url_for, session
from http import HTTPStatus
import funciones.funciones
import secrets

app = Flask(__name__)
app.secret_key = 'c13d6b2d33bc0b22412c0c723fe5acdd2fb3c941052ce7aed61be9e6cb457d1e'

@app.route("/")
def retornar():
  return redirect(url_for("index"),Response=HTTPStatus.OK) 

@app.route("/peliculas.html",methods=["GET"])
@app.route("/peliculas",methods=["GET"])
def index():
  if 'username' in session:
    user = session['username']
  else:
    user = ""
  return Response (render_template("peliculas.html", user=user, 
  nombre_peliculas=funciones.funciones.nombresPeliculas(), 
  imagenes_peliculas=funciones.funciones.imgPeliculas()), status = HTTPStatus.OK)

@app.route("/buscar/<int:info>",methods=["GET"])
@app.route("/buscar/<info>",methods=["GET"])
def buscar(info):
    lista_encontradas=[]
    peliculas = funciones.funciones.moviesFiles()
    for i in peliculas[::-1]:
        #print(i.values())
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

@app.route('/perfil', methods=['GET', 'POST'])
def login():
  if 'username' in session:
    return redirect(url_for('index'))
  if request.method == 'POST':
    dataUser = {
      "username": request.form['username'],
      "password": request.form['password']
    }
    users = controller.funciones.usersFiles()
    for user in users:
      if dataUser["username"] == user["Usuario"] and dataUser["password"] == user["Contrasenia"]:
        session["username"] = dataUser['username']
        user = dataUser['username']
      else:
        user = ""
    return Response (render_template("peliculas.html", user=user, nombre_peliculas=funciones.funciones.nombresPeliculas(), imagenes_peliculas=controller.funciones.imgPeliculas()), status = HTTPStatus.OK)
  return render_template('perfil.html')

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
      return render_template('comentarios.html', unaPeli=unaPeli, user=funciones.funciones.verify())
  
@app.route('/pelicula/agregar', methods=['GET', 'POST'])
def add_Pelicula():
  if request.method == 'POST':
    pelicula = {
        "id":secrets.token_hex(),
        "nombre":request.form['Nombre'],
        "anio":request.form['Anio'],
        "fecha_estreno":request.form['Estreno'],
        "director":request.form['Director'],
        "genero":request.form['Genero'],
        "img":request.form['img'],
        "comentarios":[],
        "sinopsis":request.form['Sinopsis']
    }
    funciones.funciones.agregarPeliculas(pelicula)
  return render_template('agregarPeli.html', directores=funciones.funciones.directores, generos=funciones.funciones.generos)

if __name__ == "__main__":
  app.run(debug=True)