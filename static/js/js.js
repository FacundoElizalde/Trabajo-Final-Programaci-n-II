const eliminar = document.querySelector(".del_pelicula");
const eliminacion = document.querySelector("#eliminacion");
const editar = document.querySelector('.edit_pelicula');
const edicion = document.querySelector('#edicion');
document.addEventListener('DOMContentLoaded',e => {
  if (e.path[0].URL.includes("http://127.0.0.1:5000/pelicula/editar/")) {
    const inicio = editar;
    init(inicio)
  }
  else if (e.path[0].URL.includes("http://127.0.0.1:5000/pelicula/eliminar/")) {
    const inicio = eliminar;
    init(inicio)
  }
  else{
    return null
  }
})


async function init(inicio){
  await inicio.addEventListener("click", e => {
    e.preventDefault();
    const pelicula = e.target.value;
    if (e.target.className === "eliminarPeli") {
      const form = {
        formulario:`
        <label for="eliminar">Esta seguro que desea eliminar: <strong>${pelicula}</strong>? presione eliminar para completar, de lo contrario vuelva al inicio.</label>
        <input type="submit" value="Eliminar" name="eliminar">
        `,
        clas:"eliminar_peli",
        desde: eliminar,
        hacia: eliminacion
      }
      mensaje(form);
    } else {
      const form = {
        formulario:`
        <div>
          <label for="nombre">Nombre de la pelicula:</label>
          <input type="text" name="nombre">
        </div>
        <div>
          <label for="imagen">Imagen:</label>
          <input type="text" name="imagen" required placeholder="La URL de la imagen">
        </div>
        <div>
          <label for="anio">Anio:</label>
          <input type="text" name="anio">
        </div>
        <div>
          <label for="estreno">Fecha de estreno:</label>
          <input type="text" name="estreno" placeholder="1 de Septiembre" required>
        </div>
        <div>
          <label for="estreno">Sinopsis</label>
          <input type="text" name="sinopsis" required>
        </div>
        <div>
            <label for="nombre">Directores disponibles</label>
            <select name="director" required>
            <option value="Louis Leterrier">Louis Leterrier</option>
            </select>
          </div>

          <div>
            <label for="nombre">Generos disponibles</label>
            <select name="genero" required>
            <option value="accion">accion</option>
            </select>
          </div>
          
        <input type="submit" value="editar">
        `,
        clas:"edit_pelicula",
        desde:editar,
        hacia:edicion
      }
      mensaje(form)
    }
  });
}

function mensaje(form){
  const { formulario, clas, desde, hacia } = form;
  desde.remove();
  const exist = document.querySelector("#alerta-roja");
  if (!exist) {
    const msj = document.createElement("form");
    msj.classList.add(clas);
    msj.id = "alerta-roja";
    msj.method = "POST";
    msj.innerHTML = formulario;
    hacia.appendChild(msj);
  }
}