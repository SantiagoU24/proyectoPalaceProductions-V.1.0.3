# funciones.py
from flask import Flask, session, request, render_template, redirect, Response, url_for
from database import mysql

app = Flask(__name__, template_folder='templates', static_folder='static')

#FUNCION LOGIN
def login(request):
    if request.method == 'POST' and 'txtCorreo' in request.form and 'txtPassword' in request.form:
        _correo = request.form['txtCorreo']
        _password = request.form['txtPassword']

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE correo = %s AND contrasena = %s', (_correo, _password,))
        account = cur.fetchone()
        cur.close()

        if account:
            session['logueado'] = True
            session['id'] = account['id_usuario']
            session['rol'] = account['id_rol']
            return True  # Autenticación exitosa
    return False  # Autenticación fallida

#FUNCION REGISTRO USUARIOS
def crear_registro():
    if request.method == 'POST':
        nombre = request.form['txtNombre']
        apellido = request.form['txtApellido']
        tipoDocumento = request.form['txtTipoDoc']
        numeroDocumento = request.form['txtNumeroDocumento']
        correo = request.form['txtCorreo']
        fechaNacimiento = request.form['txtFechaNacimiento']
        celular = request.form['txtNumeroTelefono']
        password = request.form['txtPassword']
       
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Usuarios (nombres, apellidos, tipo_documento, numero_documento, correo, fecha_de_nacimiento ,celular,  contrasena, id_rol) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,'2')",
                    (nombre, apellido, tipoDocumento, numeroDocumento, correo, fechaNacimiento ,celular, password))
        mysql.connection.commit()
        cur.close()

        return 'Registro insertado correctamente'


#FUNCION AGENDAMIENTO CITAS
def formulario_reservas():
    if request.method == 'POST':
        nombre = request.form['nombre']
        fecha = request.form['fecha']
        hora = request.form['hora']
        correo = request.form['correo']

        # Verificar si la fecha existe en la base de datos
        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM reservas WHERE fecha = %s", (fecha,))
        result = cur.fetchone()

        if result:
            # La fecha ya existe en la base de datos, verificar si la hora está disponible
            cur.execute("SELECT id FROM reservas WHERE fecha = %s AND hora = %s", (fecha, hora))
            result = cur.fetchone()
            if result:
                mensaje = 'La hora seleccionada no está disponible. Por favor, elige otra hora.'
                return render_template('formulario_reservas.html', mensaje=mensaje)
        else:
            # Insertar la reserva en la base de datos
            cur.execute("INSERT INTO reservas (nombre, fecha, hora, correo) VALUES (%s, %s, %s, %s)", (nombre, fecha, hora, correo))
            mysql.connection.commit()
            cur.close()

        return redirect(url_for('confirmacion'))

    return render_template('formulario_reservas.html')

       # return 'Registro insertado correctamente'
    

    
