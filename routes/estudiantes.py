from flask import redirect, render_template, request, session, url_for
from schemas.estudiantes import *
from models.estudiantes import *
import json

def action_required(f):
    """
    Decorador para verificar sesión de usuario antes de permitir el acceso a una ruta.
    
    Funcionamiento:
        1. Envuelve la función original para agregar validación de sesión.
        2. Si no hay usuario en sesión, redirige a la ruta raíz ('/').
        3. Si la sesión es válida, ejecuta la función original normalmente.
    """
    def wrap(*args, **kwargs):
        # Verificar existencia de usuario en sesión.
        if 'user' not in session:
            return redirect('/')    # Redirigir a raíz si no hay sesión.
        
        # Ejecutar función original si la sesión es válida.
        return f(*args, **kwargs)
    
    # Mantener el nombre original de la función.
    wrap.__name__ = f.__name__
    return wrap

def rutasDeEstudiantes(app):
    """
    Configura todas las rutas relacionadas con los estudiantes en la aplicación web.
    Incluye manejo de:
        - Envío de solicitudes.
        - Administración y modificación de datos personales.
    """

    @app.route('/estudiante/inicio', methods = ['GET'])
    @action_required    # Decorador que verifica sesión activa.
    def student_home():
        """
        Ruta principal del dashboard estudiantil que muestra:
            1. Información personal del usuario.
            2. Horarios académicos del estudiante.
        """
        usuario = session.get("user")   # Datos almacenados durante el login.
        horarios_r = horarios() # Consulta de horarios académicos.
        return render_template('student_1.html', usuario = usuario, horarios = horarios_r)
    
    @app.route('/estudiante/vale', methods = ['GET'])
    @action_required    # Decorador que verifica sesión activa.
    def student_voucher():
        """
        Página de generación de vales de estudiante.
        
        Proceso:
            Obtiene y actualiza los datos del estudiante.
            Recopila todos los datos necesarios para el formulario:
                - Listado de maestros registrados.
                - Materiales disponibles por laboratorio.
                - Fecha actual del sistema.
        """
        # Datos almacenados durante el login.
        usuario = session.get("user")
        resultado = obtenerEstudianteDB(usuario[0])
        usuario = session["user"] = resultado[:-1]

        # Obtiene datos para los selectores del formulario.
        maestros = maestros_registrados()
        materiales = material_registrado_estudiante()
        horarios = obtener_horario()
        return render_template('student_2.html', usuario = usuario, maestros = maestros, materiales = materiales, fecha = horarios[0])
    
    @app.route('/estudiante/vale/enviado', methods = ['POST'])
    @action_required    # Decorador que verifica sesión activa.
    def student_voucher_1():
        """
        Maneja el envío de vales de laboratorio/proyecto por parte de estudiantes.
        
        Flujo principal:
            1. Valida restricciones de vales existentes.
            2. Genera identificador único para el vale.
            3. Actualiza contadores de vales del estudiante.
            4. Registra la solicitud en la base de datos.
            5. Retorna respuesta JSON con resultado.
        """

        # Obtiene datos de usuario y solicitud.
        usuario = session.get("user")
        data = request.json
        vale = data.get('vale')

        # Validación de vale de laboratorio existente.
        if vale == 'LABORATORIO' and usuario[1] == '1':
            return {"status": "error",'mensaje': 'Ya tienes un vale de Laboratorio'}
        else:
            # Procesamiento del vale.
            ncontrol = usuario[0]   # Número de control del estudiante.
            horarios = obtener_horario()    # Obtiene fecha/hora actual.
            identificacion = crear_identificacion(ncontrol, vale, horarios)  # Genera ID único.

            # Verifica si el vale ya existe.
            resultado = vale_existente_estudiante(identificacion)
            if resultado:
                return {"status": "error",'mensaje': 'Ya tienes un vale Agregado'}
            else:
                # Actualiza contadores según tipo de vale.
                if vale == 'LABORATORIO':
                    vales_cantidad(vale, '1', ncontrol)
                    session["user"] = (usuario[0], '1', usuario[2], usuario[3], usuario[4], usuario[5], usuario[6])
                elif vale == 'PROYECTO':
                    cantidad = int(usuario[2])
                    cantidad = str(cantidad + 1)
                    vales_cantidad(vale, cantidad, ncontrol)
                    session["user"] = (usuario[0], usuario[1], cantidad, usuario[3], usuario[4], usuario[5], usuario[6])

                # Prepara datos para registro.
                estado = 'SIN ACEPTAR'
                materia = data.get('materia')
                grupo = data.get('grupo')
                profesor = data.get('profesor')
                alumnos = data.get('alumnos')
                laboratorio = data.get('laboratorio')
                items = data.get('items')

                # Procesa numeración de equipos del laboratorio.
                resultado = obtener_numeracion_laboratorio(laboratorio)
                resultado = compara_y_agrega(items, resultado)
                material = json.dumps(resultado)

                # Registra la solicitud en la base de datos.
                registrarSolicitudEstudiante(identificacion, ncontrol, horarios[1], horarios[0], usuario[5], usuario[6], profesor, materia, grupo, alumnos, laboratorio, estado, vale, material)
                return {"status": "redirect", "url": url_for('student_voucher'), 'mensaje': 'Vale Enviado Exitosamente'}
    
    @app.route('/estudiante/historial', methods = ['GET'])
    @action_required    # Decorador que verifica sesión activa.
    def student_register():
        """
        Muestra el historial de vales solicitados por el estudiante.
        
        Proceso:
            Obtiene todas las solicitudes del estudiante.
            Procesa los materiales de cada solicitud.
        """
        usuario = session.get("user")

        # Recupera todas las solicitudes del estudiante usando su número de control.
        solicitudes = valesSolicitadosEstudiantes(usuario[0])

        # Procesa los materiales de cada solicitud.
        material = {}
        for solicitud in solicitudes:
            k = json.loads(solicitud[16])
            material[solicitud[0]] = k
        return render_template('student_3.html', usuario = usuario, solicitudes = solicitudes, material = material)
    
    @app.route('/estudiante/historial/eliminar', methods = ['POST'])
    @action_required    # Decorador que verifica sesión activa.
    def student_register_1():
        """
        Proceso para eliminar una solicitud de vale de estudiante y actualizar sus contadores.

        Flujo:
            Valida que la solicitud exista.
            Actualiza contadores según tipo de vale:
                - LABORATORIO: Restablece contador a 0.
                - PROYECTO: Decrementa contador en 1.
            Elimina la solicitud de la base de datos.

        Parámetros:
            identificacion: ID único de la solicitud a eliminar.

        Retorna un JSON con:
            - status: "alerta" o "error".
            - mensaje: Descripción del resultado.
        """
        # Obtiene datos de usuario y solicitud.
        usuario = session.get("user")
        data = request.json
        identificacion = data.get('identificacion')

        # Verifica existencia de la solicitud.
        resultado = vale_existente_estudiante(identificacion)
        if resultado:

            # Actualiza contadores según tipo de vale.
            if resultado[14] == 'LABORATORIO':
                vales_cantidad(resultado[14], '0', usuario[0])
                session["user"] = (usuario[0], '0', usuario[2], usuario[3], usuario[4], usuario[5], usuario[6])
            elif resultado[14] == 'PROYECTO':
                cantidad = int(usuario[2])
                cantidad = str(cantidad - 1)
                vales_cantidad(resultado[14], cantidad, usuario[0])
                session["user"] = (usuario[0], usuario[1], cantidad, usuario[3], usuario[4], usuario[5], usuario[6])

            # Elimina la solicitud.
            eliminarSolicitudEstudiante(identificacion)
            return {"status": "alerta",'mensaje': 'Solicitud Eliminada'}
        else:
            return {"status": "error",'mensaje': 'Solicitud Inexistente'}
    
    @app.route('/estudiante/perfil', methods = ['GET'])
    @action_required    # Decorador que verifica sesión activa.
    def student_profile():
        """
        Muestra la página de perfil del estudiante.
        """
        usuario = session.get("user")
        return render_template('student_4.html', usuario = usuario)
    
    @app.route('/estudiante/perfil/datos', methods = ['POST'])
    @action_required    # Decorador que verifica sesión activa.
    def student_profile_1():
        """
        Metodo para actualizar los datos personales del estudiante (nombres y apellidos).

        Flujo:
            Obtiene datos actualizados del request JSON.
            Actualiza la base de datos.
            Refleja cambios en la sesión.
            Retorna confirmación al cliente.

        Parámetros:
            nombres: Nuevo nombre(s) del estudiante.
            apellidos: Nuevo apellido(s) del estudiante.

        Retorna un JSON con:
            - status: "exito".
            - mensaje: Datos Actualizados.
        """
        # Extrae nuevos datos del cuerpo JSON.
        usuario = session.get("user")
        data = request.json
        ncontrol = usuario[0]
        nombres = data.get('nombres')
        apellidos = data.get('apellidos')

        # Actualiza base de datos.
        actualizarDatosEstudianteDB(nombres, apellidos, ncontrol)

        # Actualiza la sesión del usuario.
        session["user"] = (usuario[0], usuario[1], usuario[2], usuario[3], usuario[4], nombres, apellidos)
        return {"status": "exito",'mensaje': 'Datos Actualizados', 'informacion': [nombres, apellidos]}
    
    @app.route('/estudiante/perfil/llave', methods = ['POST'])
    @action_required    # Decorador que verifica sesión activa.
    def student_profile_2():
        """
        Metodo para actualizar la contraseña del estudiante.

        Flujo de operación:
            Obtiene el número de control desde la sesión activa.
            Recibe la nueva contraseña en el cuerpo de la petición.
            Actualiza la contraseña en la base de datos.
            Retorna confirmación de la operación.

        Parámetros:
            llave: Nueva contraseña.

        Retorna un JSON con:
            - status: "exito".
            - mensaje: Contraseña Actualizada.
        """
        usuario = session.get("user")

        # Extrae nuevos datos del cuerpo JSON.
        data = request.json
        ncontrol = usuario[0]
        llave = data.get('llave')

        # Actualiza la contraseña en la base de datos.
        actualizarLlaveEstudianteDB(llave, ncontrol)
        return {"status": "exito",'mensaje': 'Contraseña Actualizada'}