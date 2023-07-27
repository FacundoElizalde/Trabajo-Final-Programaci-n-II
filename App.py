from flask import Flask,request,Response,render_template,redirect,url_for, session
from http import HTTPStatus
import json
from funciones.funciones import nombresPeliculas, imgPeliculas, usersFiles, moviesFiles

usuario_privado=""
app = Flask(__name__)
app.secret_key = 'secretKey1234567890'

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
  return Response (render_template("peliculas.html", user=user, nombre_peliculas=nombresPeliculas(), imagenes_peliculas=imgPeliculas()), status = HTTPStatus.OK)

@app.route("/buscar/<int:info>",methods=["GET"])
@app.route("/buscar/<info>",methods=["GET"])
def buscar(info):
    lista_encontradas=[]
    peliculas = moviesFiles()
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
    users = usersFiles()
    for user in users:
      if dataUser["username"] == user["Usuario"] and dataUser["password"] == user["Contrasenia"]:
        session["username"] = dataUser['username']
        user = dataUser['username']
      else:
        user = ""
    return Response (render_template("peliculas.html", user=user, nombre_peliculas=nombresPeliculas(), imagenes_peliculas=imgPeliculas()), status = HTTPStatus.OK)
  return render_template('perfil.html')


@app.route('/logout')
def logout():
  session.pop('username', None)
  return redirect(url_for('index'))

if __name__ == "__main__":
  app.run(debug=True)