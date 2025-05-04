from flask import redirect, render_template, request, session, url_for
# from schemas.estudiantes import *
from models.administrador import *
import json

def action_required_a(f):
    """
    Decorador para verificar sesión de administrador antes de permitir el acceso a una ruta.
    
    Funcionamiento:
        1. Envuelve la función original para agregar validación de sesión.
        2. Si no hay administrador en sesión, redirige a la ruta raíz ('/').
        3. Si la sesión es válida, ejecuta la función original normalmente.
    """
    def wrap(*args, **kwargs):
        # Verificar existencia de usuario en sesión.
        if 'admin' not in session:
            return redirect('/')    # Redirigir a raíz si no hay sesión.
        
        # Ejecutar función original si la sesión es válida.
        return f(*args, **kwargs)
    
    # Mantener el nombre original de la función.
    wrap.__name__ = f.__name__
    return wrap

def rutasDeAdministrador(app, socketio):
    @app.route('/administrador/inicio', methods = ['GET'])
    @action_required_a    # Decorador que verifica sesión activa.
    def admin_home():
        admin = session.get("admin")   # Datos almacenados durante el login.
        horarios_r = horarios() # Consulta de horarios académicos.
        return render_template('admin_1.html', admin = admin, horarios = horarios_r)
    
    @app.route('/administrador/inicio/actualizar', methods = ['POST'])
    @action_required_a    # Decorador que verifica sesión activa.
    def admin_home_1():
        # Datos almacenados durante el login.
        admin = session.get("admin")

        # Extrae nuevos datos del cuerpo JSON.
        data = request.json
        nombres = data.get('nombres')
        apellidos = data.get('apellidos')
        llave = data.get('llave')

        # Agrega el horario a la base de datos.
        data = [admin[0], nombres, apellidos, llave]
        session["admin"] = data[:-1]
        actualizarDatos(data)
        return {"status": "exito",'mensaje': 'Datos actualizados'}
    
    @app.route('/administrador/inicio/nuevo', methods = ['POST'])
    @action_required_a    # Decorador que verifica sesión activa.
    def admin_home_2():
        # Datos almacenados durante el login.
        admin = session.get("admin")

        # Extrae nuevos datos del cuerpo JSON.
        data = request.json
        dia = data.get('dia')
        laboratorio = data.get('lab')
        inicio = data.get('hora1')
        final = data.get('hora2')

        # Agrega el horario a la base de datos.
        data = [dia, laboratorio, inicio, final]
        agregarHorario(data)
        return {"status": "exito",'mensaje': 'Horario agregado'}
    
    @app.route('/administrador/inicio/eliminar', methods = ['POST'])
    @action_required_a    # Decorador que verifica sesión activa.
    def admin_home_3():
        # Extrae nuevos datos del cuerpo JSON.
        data = request.json
        data = [data['dia'], data['lab'], data['inicio'], data['fin']]

        # Elimina el horario de la base de datos.
        eliminarHorario(data)
        return {"status": "exito",'mensaje': 'Horario eliminado'}