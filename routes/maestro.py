from flask import redirect, render_template, request, session, url_for
from models.maestro import *
from schemas.maestro import *
import json

def action_required_t(f):
    """
    Decorador para verificar sesión de maestro antes de permitir el acceso a una ruta.
    
    Funcionamiento:
        1. Envuelve la función original para agregar validación de sesión.
        2. Si no hay maestro en sesión, redirige a la ruta raíz ('/').
        3. Si la sesión es válida, ejecuta la función original normalmente.
    """
    def wrap(*args, **kwargs):
        # Verificar existencia de maestro en sesión.
        if 'teacher' not in session:
            return redirect('/')    # Redirigir a raíz si no hay sesión.
        
        # Ejecutar función original si la sesión es válida.
        return f(*args, **kwargs)
    
    # Mantener el nombre original de la función.
    wrap.__name__ = f.__name__
    return wrap

def rutasDeMaestro(app, socketio):
    @app.route('/maestro/inicio', methods = ['GET'])
    @action_required_t
    def teacher_home():
        maestro = session.get("teacher")
        nombre = maestro[2] + ' ' + maestro[3]
        solicitudes = valesParaMaestro(nombre)
        return render_template('teacher_1.html', maestro = maestro, solicitudes = solicitudes)
    
    @app.route('/maestro/firma', methods = ['GET'])
    @action_required_t
    def teacher_signature():
        maestro = session.get("teacher")
        nombre = maestro[2] + ' ' + maestro[3]
        solicitudes = valesParaMaestroFirma(nombre)
        material = {}
        for solicitud in solicitudes:
            k = json.loads(solicitud[16])
            material[solicitud[0]] = k
        return render_template('teacher_2.html', maestro = maestro, solicitudes = solicitudes, material = material)
    
    @app.route('/maestro/firma/aceptar', methods = ['POST'])
    @action_required_t
    def teacher_signature_1():
        usuario = session.get("user")
        data = request.json
        identificacion = data.get('identificacion')
        resultado = vale_existente_estudiante(identificacion)
        if resultado:
            valesParaMaestroAceptar(identificacion)
            return {"status": "alerta",'mensaje': 'Solicitud Aceptada'}
        else:
            return {"status": "error",'mensaje': 'Solicitud Inexistente'}
        
    @app.route('/maestro/firma/cancelar', methods = ['POST'])
    @action_required_t
    def teacher_signature_2():
        usuario = session.get("user")
        data = request.json
        identificacion = data.get('identificacion')
        solicitud = vale_existente_estudiante(identificacion)
        if solicitud:
            estudiante = obtenerEstudianteDB(solicitud[1])
            if solicitud[14] == 'LABORATORIO':
                    vales_cantidad(solicitud[14], '0', solicitud[1])
            elif solicitud[14] == 'PROYECTO':
                    if estudiante[0] != '0':
                        cantidad = int(estudiante[0])
                        cantidad = str(cantidad - 1)
                    else:
                         cantidad = '0'
                    vales_cantidad(solicitud[14], cantidad, solicitud[1])
            eliminarSolicitudEstudiante(identificacion)
            return {"status": "alerta",'mensaje': 'Solicitud Cancelada'}
        return {"status": "error",'mensaje': 'Solicitud Inexistente'}
    
    @app.route('/maestro/estudiantes/aceptados', methods = ['GET'])
    @action_required_t
    def teacher_voucher_1():
        maestro = session.get("teacher")
        nombre = maestro[2] + ' ' + maestro[3]
        solicitudes = valesParaMaestroAceptados(nombre)
        material = {}
        for solicitud in solicitudes:
            k = json.loads(solicitud[16])
            material[solicitud[0]] = k
        return render_template('teacher_3.html', maestro = maestro, solicitudes = solicitudes, material = material)
    
    @app.route('/maestro/estudiantes/registros', methods = ['GET'])
    @action_required_t
    def teacher_register():
        maestro = session.get("teacher")
        nombre = maestro[2] + ' ' + maestro[3]
        solicitudes = registroMaestros(nombre)
        material = {}
        for solicitud in solicitudes:
            k = json.loads(solicitud[18])
            material[solicitud[0]] = k
        return render_template('teacher_4.html', maestro = maestro, solicitudes = solicitudes, material = material)

    @app.route('/maestro/solicitud', methods = ['GET'])
    @action_required_t
    def teacher_request():
        maestro = session.get("teacher")
        materiales = materialMaestro()
        horarios = obtener_horario()
        return render_template('teacher_5.html', maestro = maestro, materiales = materiales, fecha = horarios[0])
    
    @app.route('/maestro/solicitud/enviar', methods = ['POST'])
    @action_required_t
    def teacher_request_1():
        maestro = session.get("teacher")
        horarios = obtener_horario()
        identificacion = crear_identificacion(maestro[0], horarios)
        solicitud = vale_existente_estudiante(identificacion)
        if solicitud:
            return {"status": "error",'mensaje': 'Solicitud Existente'}
        else:
            data = request.json
            laboratorio = data.get('laboratorio')
            items = data.get('items')
            materialAsignado(laboratorio, items)
            material = json.dumps(items)
            registrarSolicitudMaestro(identificacion, maestro[0], horarios[1], horarios[0], maestro[2], maestro[3], 'N/A', 'N/A', 'N/A', 'N/A', laboratorio, 'N/A', 'N/A', material)
            return {"status": "redirect", "url": url_for('teacher_request'), 'mensaje': 'Vale Enviado Exitosamente'}
        
    @app.route('/maestro/vales/activos', methods = ['GET'])
    @action_required_t
    def teacher_register_1():
        maestro = session.get("teacher")
        solicitudes = valesActivosMaestros(maestro[0])
        material = {}
        for solicitud in solicitudes:
            k = json.loads(solicitud[16])
            material[solicitud[0]] = k
        return render_template('teacher_6.html', maestro = maestro, solicitudes = solicitudes, material = material)
    
    @app.route('/maestro/registros', methods = ['GET'])
    @action_required_t
    def teacher_personal():
        maestro = session.get("teacher")
        solicitudes = registroMaestrosPersonal(maestro[0])
        material = {}
        for solicitud in solicitudes:
            k = json.loads(solicitud[18])
            material[solicitud[0]] = k
        return render_template('teacher_7.html', maestro = maestro, solicitudes = solicitudes, material = material)
    
    @app.route('/maestro/perfil', methods = ['GET'])
    @action_required_t
    def teacher_profile():
        maestro = session.get("teacher")
        return render_template('teacher_8.html', maestro = maestro)