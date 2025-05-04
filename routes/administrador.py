from flask import redirect, render_template, request, session, url_for, Response
from schemas.administrador import *
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
    
    @app.route('/administrador/estudiantes', methods = ['GET'])
    @action_required_a    # Decorador que verifica sesión activa.
    def admin_users():
        admin = session.get("admin")
        usuarios = estudiantesRegistrados()
        carreras = carreras_disponibles
        return render_template('admin_2.html', admin = admin, usuarios = usuarios, carreras = carreras)
    
    @app.route('/administrador/estudiantes/actualizar', methods = ['POST'])
    @action_required_a    # Decorador que verifica sesión activa.
    def admin_users_1():
        # Extrae nuevos datos del cuerpo JSON.
        data = request.json
        comprobacion = validar_correo(data[2], data[1])
        if comprobacion:
            if data[0] == data[1]:
                actualizarDatosUsuario(data)
            else:
                resultado = estudianteExistente(data[1])
                if resultado:
                    return {"status": "error",'mensaje': 'Usuario Existente'}
                else:
                    actualizarDatosUsuario(data)
            return {"status": "redirect", "url": url_for('admin_users'), 'mensaje': 'Usuario Actualizado'}
        else:
            return {"status": "error",'mensaje': 'Incongruencia en el correo y número de control'}
    
    @app.route('/administrador/estudiantes/eliminar', methods = ['POST'])
    @action_required_a    # Decorador que verifica sesión activa.
    def admin_users_2():
        # Extrae nuevos datos del cuerpo JSON.
        data = request.json
        estudianteEliminado(data)
        return {"status": "exito",'mensaje': 'Usuario Eliminado'}
    
    @app.route('/administrador/estudiantes/pdf')
    @action_required_a  # Decorador que verifica sesión activa.
    def admin_users_3():
        pdf_buffer = generarListadeEstudiantesPDF()
        return Response(
            pdf_buffer,
            mimetype='application/pdf',
            headers={"Content-Disposition": f"attachment;filename=estudiantesTECNM.pdf"}
        )
    
    @app.route('/administrador/estudiantes/csv')
    @action_required_a  # Decorador que verifica sesión activa.
    def admin_users_4():
        return Response(
            generarListadeEstudiantesCSV(),
            mimetype='text/csv',
            headers={"Content-Disposition": f"attachment;filename=estudiantesTECNM.csv"}
        )
    
    @app.route('/administrador/estudiantes/borrar', methods = ['POST'])
    @action_required_a    # Decorador que verifica sesión activa.
    def admin_users_5():
        # Extrae nuevos datos del cuerpo JSON.
        admin = session.get("admin")
        data = request.json
        resultado = administradorLlave(admin[0])
        if resultado[0] == data:
            resetearEstudiantes()
            return {"status": "redirect", "url": url_for('admin_users'), 'mensaje': 'Usuarios Eliminados'}
        else:
            return {"status": "error",'mensaje': 'Contraseña Incorrecta'}
        
    @app.route('/administrador/maestros', methods = ['GET'])
    @action_required_a    # Decorador que verifica sesión activa.
    def admin_teachers():
        admin = session.get("admin")
        maestros = maestrosRegistrados()
        return render_template('admin_3.html', admin = admin, maestros = maestros)
    
    @app.route('/administrador/maestros/actualizar', methods = ['POST'])
    @action_required_a    # Decorador que verifica sesión activa.
    def admin_teachers_1():
        # Extrae nuevos datos del cuerpo JSON.
        data = request.json
        print(data)
        if data[0] == data[1]:
            actualizarDatosMaestro(data)
        else:
            resultado = maestroExistente(data[1])
            if resultado:
                return {"status": "error",'mensaje': 'Maestro Existente'}
            else:
                actualizarDatosMaestro(data)
        return {"status": "redirect", "url": url_for('admin_teachers'), 'mensaje': 'Maestro Actualizado'}
    
    @app.route('/administrador/maestros/eliminar', methods = ['POST'])
    @action_required_a    # Decorador que verifica sesión activa.
    def admin_teachers_2():
        # Extrae nuevos datos del cuerpo JSON.
        data = request.json
        maestroEliminado(data)
        return {"status": "exito",'mensaje': 'Maestro Eliminado'}
    
    @app.route('/administrador/maestros/pdf')
    @action_required_a  # Decorador que verifica sesión activa.
    def admin_teachers_3():
        pdf_buffer = generarListadeMaestrosPDF()
        return Response(
            pdf_buffer,
            mimetype='application/pdf',
            headers={"Content-Disposition": f"attachment;filename=maestrosTECNM.pdf"}
        )
    
    @app.route('/administrador/maestros/csv')
    @action_required_a  # Decorador que verifica sesión activa.
    def admin_teachers_4():
        return Response(
            generarListadeMaestrosCSV(),
            mimetype='text/csv',
            headers={"Content-Disposition": f"attachment;filename=maestrosTECNM.csv"}
        )
    
    @app.route('/administrador/maestros/nuevo', methods = ['POST'])
    @action_required_a    # Decorador que verifica sesión activa.
    def admin_teachers_5():
        # Extrae nuevos datos del cuerpo JSON.
        data = request.json
        resultado = maestroExistente(data[0])
        if resultado:
            return {"status": "error",'mensaje': 'Identificación ya asignada'}
        else:
            agregarMaestroDB(data)
            return {"status": "redirect", "url": url_for('admin_teachers'), 'mensaje': 'Maestro Agregado'}