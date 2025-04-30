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
    """
    Configura todas las rutas relacionadas con los maestros en la aplicación web.
    Incluye manejo de:
        - Envío de solicitudes.
        - Administración de vales solicitados por estudiantes.
        - Administración de vales solicitados personales.
    """

    @app.route('/maestro/inicio', methods = ['GET'])
    @action_required_t  # Decorador que verifica sesión activa.
    def teacher_home():
        """
        Ruta principal del panel de control para maestros.

        Funcionalidades:
            Obtiene el nombre completo del maestro desde la sesión.
            Recupera estadísticas de vales asociados al maestro.
        """
        maestro = session.get("teacher")

        # Construye nombre completo.
        nombre = maestro[2] + ' ' + maestro[3]

        # Obtiene estadísticas de vales del maestro.
        solicitudes = valesParaMaestro(nombre)
        return render_template('teacher_1.html', maestro = maestro, solicitudes = solicitudes)
    
    @app.route('/maestro/firma', methods = ['GET'])
    @action_required_t  # Decorador que verifica sesión activa.
    def teacher_signature():
        """
        Ruta para mostrar las solicitudes pendientes de firma por parte del maestro.

        Flujo:
            Obtiene el nombre completo del maestro desde la sesión.
            Recupera solicitudes pendientes de firma (estado 'SIN ACEPTAR').
            Procesa los materiales de cada solicitud.
        """
        # Obtener datos del maestro desde sesión.
        maestro = session.get("teacher")
        nombre = maestro[2] + ' ' + maestro[3]

        # Obtener solicitudes pendientes de firma.
        solicitudes = valesParaMaestroFirma(nombre)

        # Procesar materiales.
        material = {}
        for solicitud in solicitudes:
            k = json.loads(solicitud[16])
            material[solicitud[0]] = k
        return render_template('teacher_2.html', maestro = maestro, solicitudes = solicitudes, material = material)
    
    @app.route('/maestro/firma/aceptar', methods = ['POST'])
    @action_required_t  # Decorador que verifica sesión activa.
    def teacher_signature_1():
        """
        Metodo para que un maestro acepte una solicitud de vale.

        Flujo:
        1. Verifica existencia de la solicitud.
        2. Si existe, cambia su estado a 'EN ESPERA'.
        3. Retorna confirmación o error.

        Parámetros:
            identificacion: ID completo del vale.

        Retorna un JSON con:
            - status: "alerta" o "error".
            - mensaje: Descripción del resultado.
        """

        # Obtención de datos.
        usuario = session.get("user")
        data = request.json
        identificacion = data.get('identificacion')

        # Verificación de existencia del vale.
        resultado = vale_existente_estudiante(identificacion)
        if resultado:

            # Actualización del estado.
            valesParaMaestroAceptar(identificacion)
            return {"status": "alerta",'mensaje': 'Solicitud Aceptada'}
        else:
            return {"status": "error",'mensaje': 'Solicitud Inexistente'}
        
    @app.route('/maestro/firma/cancelar', methods = ['POST'])
    @action_required_t  # Decorador que verifica sesión activa.
    def teacher_signature_2():
        """
        Metodo para cancelar una solicitud de vale y actualizar contadores.

        Flujo:
            Verifica existencia de la solicitud.
            Si existe:
                - Para LABORATORIO: Restablece contador a 0.
                - Para PROYECTO: Decrementa contador.
                - Elimina la solicitud.
            Retorna confirmación o error.

        Parámetros:
            identificacion: ID del vale a cancelar.
        """
        # Obtener datos básicos.
        usuario = session.get("user")
        data = request.json
        identificacion = data.get('identificacion')

        # Verificar existencia de solicitud.
        solicitud = vale_existente_estudiante(identificacion)
        if solicitud:

            # Actualizar contadores según tipo de vale.
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
            
            # Eliminar solicitud y retornar confirmación.
            eliminarSolicitudEstudiante(identificacion)
            return {"status": "alerta",'mensaje': 'Solicitud Cancelada'}
        return {"status": "error",'mensaje': 'Solicitud Inexistente'}
    
    @app.route('/maestro/estudiantes/aceptados', methods = ['GET'])
    @action_required_t  # Decorador que verifica sesión activa.
    def teacher_voucher_1():
        """
        Ruta que muestra vales de estudiantes aceptados o en espera.

        Flujo:
            Consulta vales en estado 'EN ESPERA' o 'ACTIVO'.
            Procesa los materiales de cada vale.
            Renderiza plantilla con los datos organizados.
        """
         # Obtener datos del maestro,
        maestro = session.get("teacher")
        nombre = maestro[2] + ' ' + maestro[3]

        # Obtener vales aceptados/en espera.
        solicitudes = valesParaMaestroAceptados(nombre)

        # Procesar materiales.
        material = {}
        for solicitud in solicitudes:
            k = json.loads(solicitud[16])
            material[solicitud[0]] = k
        return render_template('teacher_3.html', maestro = maestro, solicitudes = solicitudes, material = material)
    
    @app.route('/maestro/estudiantes/registros', methods = ['GET'])
    @action_required_t  # Decorador que verifica sesión activa.
    def teacher_register():
        """
        Ruta para mostrar el historial de vales registrados por el maestro.

        Flujo:
            Consulta vales registrados.
            Procesa materiales.
            Renderiza plantilla con datos organizados.
        """
        # Obtener información del maestro.
        maestro = session.get("teacher")
        nombre = maestro[2] + ' ' + maestro[3]

        # Obtener registros de vales.
        solicitudes = registroMaestros(nombre)

        # Procesar materiales.
        material = {}
        for solicitud in solicitudes:
            k = json.loads(solicitud[18])
            material[solicitud[0]] = k
        return render_template('teacher_4.html', maestro = maestro, solicitudes = solicitudes, material = material)

    @app.route('/maestro/solicitud', methods = ['GET'])
    @action_required_t  # Decorador que verifica sesión activa.
    def teacher_request():
        """
        Ruta para mostrar el formulario de solicitud de materiales para maestros.

        Flujo:
            Consulta materiales disponibles.
            Obtiene fecha actual.
        """
        maestro = session.get("teacher")
        materiales = materialMaestro()
        horarios = obtener_horario()
        return render_template('teacher_5.html', maestro = maestro, materiales = materiales, fecha = horarios[0])
    
    @app.route('/maestro/solicitud/enviar', methods = ['POST'])
    @action_required_t  # Decorador que verifica sesión activa.
    def teacher_request_1():
        """
        Metodo para procesar el envío de solicitudes de materiales por parte de maestros.

        Flujo:
            Genera ID único para la solicitud.
            Verifica que no exista una solicitud duplicada.
            Procesa asignación de materiales.
            Registra la solicitud con estado automático.
            Retorna confirmación o error.
        """
        # Preparar datos base.
        maestro = session.get("teacher")
        horarios = obtener_horario()
        identificacion = crear_identificacion(maestro[0], horarios)

        # Validar solicitud única.
        solicitud = vale_existente_estudiante(identificacion)
        if solicitud:
            return {"status": "error",'mensaje': 'Solicitud Existente'}
        else:
            # Procesar datos del formulario.
            data = request.json
            laboratorio = data.get('laboratorio')
            items = data.get('items')

            # Registrar materiales y solicitud.
            materialAsignado(laboratorio, items)
            material = json.dumps(items)
            registrarSolicitudMaestro(identificacion, maestro[0], horarios[1], horarios[0], maestro[2], maestro[3], 'N/A', 'N/A', 'N/A', 'N/A', laboratorio, 'N/A', 'N/A', material)
            return {"status": "redirect", "url": url_for('teacher_request'), 'mensaje': 'Vale Enviado Exitosamente'}
        
    @app.route('/maestro/vales/activos', methods = ['GET'])
    @action_required_t  # Decorador que verifica sesión activa.
    def teacher_register_1():
        """
        Ruta para mostrar los vales activos registrados por el maestro.

        Flujo:
            Consulta vales activos asociados a su ID.
            Procesa los materiales de cada vale.
            Renderiza plantilla con los datos organizados.
        """
         # Obtener datos del maestro desde sesión.
        maestro = session.get("teacher")

        # Consultar vales activos.
        solicitudes = valesActivosMaestros(maestro[0])

        # Procesar materiales.
        material = {}
        for solicitud in solicitudes:
            k = json.loads(solicitud[16])
            material[solicitud[0]] = k
        return render_template('teacher_6.html', maestro = maestro, solicitudes = solicitudes, material = material)
    
    @app.route('/maestro/registros', methods = ['GET'])
    @action_required_t  # Decorador que verifica sesión activa.
    def teacher_personal():
        """
        Ruta para mostrar los vales registrados por el maestro.

        Flujo:
            Consulta vales activos asociados a su ID.
            Procesa los materiales de cada vale.
            Renderiza plantilla con los datos organizados.
        """
         # Obtener datos del maestro desde sesión.
        maestro = session.get("teacher")

        # Consultar vales activos.
        solicitudes = registroMaestrosPersonal(maestro[0])

        # Procesar materiales.
        material = {}
        for solicitud in solicitudes:
            k = json.loads(solicitud[18])
            material[solicitud[0]] = k
        return render_template('teacher_7.html', maestro = maestro, solicitudes = solicitudes, material = material)
    
    @app.route('/maestro/perfil', methods = ['GET'])
    @action_required_t  # Decorador que verifica sesión activa.
    def teacher_profile():
        """
        Ruta para mostrar el perfil del maestro.

        Flujo:
            Obtiene los datos del maestro desde la sesión.
        """
        maestro = session.get("teacher")
        return render_template('teacher_8.html', maestro = maestro)