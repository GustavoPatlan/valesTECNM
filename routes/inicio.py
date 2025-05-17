from flask import redirect, render_template, request, session, url_for
from models.inicio import *
from schemas.inicio import *

def rutasDeInicio(app):
    """
    Configura todas las rutas relacionadas con la autenticación en la aplicación web.
    Incluye manejo de:
        - Inicio de sesión.
        - Registro de nuevos usuarios.
        - Recuperación de contraseñas.
    """

    @app.route('/')
    def index():
        """
        Ruta raíz que redirige automáticamente a la página de inicio de sesión.
        """
        return redirect('/inicio')
    
    @app.route('/inicio')
    def login():
        """
        Muestra la página de inicio de sesión.
        Limpia cualquier dato existente en la sesión para empezar un nuevo ciclo de autenticación.
        """
        session.clear()
        return render_template('login.html')
    
    @app.route('/inicio/entrar', methods=['POST'])
    def login_in():
        """
        Procesa el formulario de inicio de sesión.
        Valida las credenciales contra la base de datos y redirige según el tipo de usuario.

        Espera un JSON con:
            - identificador: Número de control o ID.
            - llave: Contraseña.
            - usuario: Tipo de usuario (Estudiante, Maestro, Casetero o Administrador).

        Retorna un JSON con:
            - status: "redirect", "error" o "alerta".
            - mensaje: Descripción del resultado.
            - url: Ruta a redirigir.
        """
        # Obtener datos de la solicitud.
        data = request.json
        identificador = data.get('identificador')
        usuario = data.get('usuario')

        # Verifica si el usuario ya existe.
        resultado = usuarioInicio(identificador, usuario)
        if resultado:
            llave = data.get('llave')

            # Valida la contraseña.
            if resultado[-1] != llave:
                return {"status": "alerta",'mensaje': 'Contraseña Incorrecta.'}
            else:
                mensaje = 'Inicio de Sesión Exitoso.'
                match usuario:
                    case 'Estudiante':
                        session["user"] = resultado[:-1]
                        return {"status": "redirect", "url": url_for('student_home'), 'mensaje': mensaje }
                    case 'Maestro':
                        session["teacher"] = resultado[:-1]
                        return {"status": "redirect", "url": url_for('teacher_home'), 'mensaje': mensaje }
                    case 'Casetero':
                        session["worker"] = resultado[:-1]
                        return {"status": "redirect", "url": url_for('worker_home'), 'mensaje': mensaje }
                    case 'Admin':
                        session["admin"] = resultado[:-1]
                        return {"status": "redirect", "url": url_for('admin_home'), 'mensaje': mensaje }
        else:
            return {"status": "error",'mensaje': 'Usuario Inexistente.'}
    
    @app.route('/registro')
    def register():
        """
        Muestra el formulario de registro para nuevos estudiantes.
        Incluye la lista de carreras disponibles para seleccionar.
        """
        session.clear()
        carreras = carreras_disponibles
        return render_template('register.html', carreras = carreras)
    
    @app.route('/registro/codigo', methods=['POST'])
    def register_code():
        """
        Primera etapa del registro:
        1. Verifica que el número de control no esté registrado.
        2. Valida el formato del correo institucional.
        3. Verifica que la carrera sea válida.
        4. Genera y envía un código de verificación.

        Espera un JSON con:
            - identificador: Número de control o ID.
            - correo: Correo electrónico institucional.
            - carrera: Carrera seleccionada.

        Retorna un JSON con status y mensaje:
            - error: Cuando falla alguna validación.
            - notificacion: Cuando se envía el código exitosamente.
        """
        # Obtener y validar datos de la solicitud.
        data = request.json
        identificador = data.get('identificador')

        # Verificar si el usuario ya existe.
        resultado = usuarioInicio(identificador)
        if resultado:
            return {"status": "error",'mensaje': 'Número de control ya registrado.'}
        else:
            correo = data.get('correo')

            # Validar correo institucional.
            if validar_correo(correo, identificador):
                carrera = data.get('carrera')

                # Validar carrera disponible.
                if carrera in carreras_disponibles:

                    # Generar y almacenar código de verificación.
                    session["code"] = patron = generar_codigo(6)

                    # Enviar correo.
                    mandar_correo(patron, correo)
                    return {"status": "notificacion",'mensaje': 'Codigo Enviado.'}
                else:
                    return {"status": "error",'mensaje': 'La carrera no está disponible.'}
            else:
                return {"status": "error",'mensaje': 'Formato de correo incorrecto.'}
    
    @app.route('/registro/codigo/verificar', methods=['POST'])
    def register_code_check():
        """
        Segunda etapa del registro para verificar el código de confirmación y completar el registro del estudiante:
        1. Verifica que el código ingresado coincida con el almacenado en sesión.
        2. Si es correcto, registra al estudiante en la base de datos.
        3. Limpia la sesión y redirige al login.
        4. Si falla, devuelve un mensaje de error.

        Espera un JSON con:
            - codigo: Código de verificación ingresado por el usuario.
            - identificador: Número de control.
            - correo: Correo institucional.
            - carrera: Carrera seleccionada.
            - nombre: Nombre(s) del estudiante.
            - apellido: Apellido(s) del estudiante.
            - llave: Contraseña.

        Retorna un JSON con:
            - status: "redirect" o "error".
            - mensaje: Descripción del resultado.
            - url: Ruta a redirigir.
        """
        # Obtener datos de la solicitud.
        data = request.json
        codigo = data.get('codigo')
        codigoSesion = session.get("code")

        # Validar coincidencia de códigos.
        if codigo != codigoSesion:
            return {"status": "error",'mensaje': 'Codigo Incorrecto.'}
        elif codigo == codigoSesion:

            # Extraer todos los datos del formulario.
            identificador = data.get('identificador')
            correo = data.get('correo')
            carrera = data.get('carrera')
            correo = data.get('correo')
            nombre = data.get('nombre')
            apellido = data.get('apellido')
            llave = data.get('llave')

            # Registrar en base de datos.
            registrarEstudianteDB(identificador, correo, carrera, nombre, apellido, llave)

            # Limpiar sesión.
            session.clear()
            return {"status": "redirect", "url": url_for('login'), 'mensaje': 'Usuario registrado exitosamente.'}
        return {"status": "error",'mensaje': 'Error en el proceso.'}
    
    @app.route('/llave')
    def password():
        """
        Muestra la página para la recuperación de contraseña.
        """
        return render_template('password.html')
    
    @app.route('/llave/confirmar', methods=['POST'])
    def password_check():
        """
        Primera etapa para confirmar un correo electrónico y enviar código de recuperación.
        1. Recibe un correo electrónico.
        2. Verifica si el correo existe en la base de datos.
        3. Si existe:
            - Genera un código de 6 dígitos.
            - Almacena el código en la sesión.
            - Envía el código por correo electrónico.
            - Retorna confirmación.
        4. Si no existe, retorna error.

        Espera un JSON con:
            - correo: Dirección de correo a verificar.

        Retorna un JSON con:
            - status: "notificacion" o "error".
            - mensaje: Descripción del resultado.
        """
        # Obtener datos de la solicitud.
        data = request.json
        correo = data.get('correo')

        # Verificar si el correo existe en la base de datos
        resultado = obtenerEstudianteDB(correo)
        if resultado:

            # Generar y almacenar código de verificación.
            session["code"] = patron = generar_codigo(6)

            # Enviar correo.
            mandar_correo(patron, correo)
            return {"status": "notificacion",'mensaje': 'Codigo Enviado.'}
        else:
            return {"status": "error",'mensaje': 'Correo no registrado.'}
        
    @app.route('/llave/cambiar', methods=['POST'])
    def password_change():
        """
        Segunda etapa para cambiar la contraseña de un estudiante después de verificar el código.
        1. Verifica que el código proporcionado coincida con el almacenado en sesión.
        2. Si es correcto:
            - Actualiza la contraseña en la base de datos.
            - Limpia la sesión.
            - Redirige al login con mensaje de éxito.
        3. Si falla:
            - Retorna mensajes de error específicos.

        Espera un JSON con:
            - codigo: Código de verificación.
            - correo: Correo del estudiante.
            - llave: Nueva contraseña.

        Retorna un JSON con:
            - status: "redirect" o "error".
            - mensaje: Descripción del resultado.
            - url: Ruta a redirigir.
        """
        # Obtener datos de la solicitud.
        data = request.json
        codigo = data.get('codigo')

        # Validar código de verificación.
        codigoSesion = session.get("code")
        if codigo != codigoSesion:
            return {"status": "error",'mensaje': 'Codigo Incorrecto.'} 
        elif codigo == codigoSesion:

            # Procesar cambio de contraseña.
            correo = data.get('correo')
            llave = data.get('llave')
            
            # Actualizar contraseña en la base de datos.
            actualizarLlaveEstudianteDB(llave, correo)

            # Limpiar sesión por seguridad.
            session.clear()
            return {"status": "redirect", "url": url_for('login'), 'mensaje': 'Cambio de contraseña exitoso.'}
        return {"status": "error",'mensaje': 'Fallo en la modificación.'}