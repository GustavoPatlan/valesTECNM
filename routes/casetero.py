from flask import redirect, render_template, request, session, url_for, Response, jsonify
from models.casetero import *
from schemas.casetero import *
import json

def action_required_w(f):
    """
    Decorador para verificar sesión de casetero antes de permitir el acceso a una ruta.
    
    Funcionamiento:
        1. Envuelve la función original para agregar validación de sesión.
        2. Si no hay maestro en sesión, redirige a la ruta raíz ('/').
        3. Si la sesión es válida, ejecuta la función original normalmente.
    """
    def wrap(*args, **kwargs):
        # Verificar existencia de maestro en sesión.
        if 'worker' not in session:
            return redirect('/')    # Redirigir a raíz si no hay sesión.
        
        # Ejecutar función original si la sesión es válida.
        return f(*args, **kwargs)
    
    # Mantener el nombre original de la función.
    wrap.__name__ = f.__name__
    return wrap

def rutasDeTrabajador(app):
    """
    Configura todas las rutas relacionadas con los caseteros en la aplicación web.
    Incluye manejo de:
        - Asignación de material.
        - Edición de material.
        - Manejo de registros.
        - Administración de vales solicitados por estudiantes.
        - Administración de vales solicitados por maestros.
    """

    @app.route('/casetero/inicio', methods = ['GET'])
    @action_required_w  # Decorador que verifica sesión activa.
    def worker_home():
        casetero = session.get("worker")

        # Obtiene estadísticas de vales del maestro.
        solicitudes = valesParaCasetero(casetero[3])
        return render_template('worker_1.html', casetero = casetero, solicitudes = solicitudes)
    
    @app.route('/casetero/vales/activos', methods = ['GET'])
    @action_required_w  # Decorador que verifica sesión activa.
    def worker_voucher_1():
        """
        Ruta para mostrar las solicitudes activas de los estudiantes en un laboratorio en específico.

        Flujo:
            Obtiene el laboratorio asignado al casetero.
            Recupera solicitudes activas.
            Procesa los materiales de cada solicitud.
        """
        # Obtener datos del casetero desde sesión.
        casetero = session.get("worker")

        # Obtener solicitudes activas.
        solicitudes = valesParaCaseteroActivo(casetero[3])

        # Procesar materiales.
        material = {}
        for solicitud in solicitudes:
            k = json.loads(solicitud[16])
            material[solicitud[0]] = k
        return render_template('worker_2.html', casetero = casetero, solicitudes = solicitudes, material = material)
    
    @app.route('/casetero/vales/activos/reporte', methods = ['POST'])
    @action_required_w  # Decorador que verifica sesión activa.
    def worker_voucher_1_1():
        """
        Metodo para que el personal de casetero registre reportes sobre vales activos.

        Flujo:
            Recibe ID del vale y texto del reporte.
            Actualiza el registro en la base de datos.
            Retorna confirmación de la operación.

        Retorna un JSON con:
            - status: "exito".
            - mensaje: Descripción del resultado.
        """
        # Obtención de datos.
        casetero = session.get("worker")
        data = request.json
        identificacion = data.get('identificacion')
        reporte = data.get('reporte')

        # Agregar reporte al vale correspondiente.
        reportarVale(identificacion, reporte)
        return {"status": "exito",'mensaje': 'Reporte Asignado'}
    
    @app.route('/casetero/vales/activos/cancelar', methods = ['POST'])
    @action_required_w  # Decorador que verifica sesión activa.
    def worker_voucher_1_2():
        """
        Metodo para que el personal de casetero cancele reportes sobre vales activos.

        Flujo:
            Recibe ID del vale.
            Actualiza el registro en la base de datos.
            Retorna confirmación de la operación.

        Retorna un JSON con:
            - status: "exito".
            - mensaje: Descripción del resultado.
        """
        # Obtención de datos.
        casetero = session.get("worker")
        data = request.json
        identificacion = data.get('identificacion')

        # Cancela el reporte al vale correspondiente.
        reportarVale(identificacion)
        return {"status": "exito",'mensaje': 'Reporte Cancelado'}
    
    @app.route('/casetero/vales/activos/finalizar', methods = ['POST'])
    @action_required_w  # Decorador que verifica sesión activa.
    def worker_voucher_1_3():
        """
        Metodo para finalizar vales activos y actualizar registros.

        Flujo:
            Verifica existencia del vale.
            Obtiene el nombre del casetero en turno que finaliza el vale.
            Actualiza contadores según tipo de vale:
                - LABORATORIO: Restablece a 0.
                - PROYECTO: Decrementa en 1.
            Registra el vale finalizado en historial
            Retorna confirmación para redirección

        Parámetros.:
            identificacion: ID del vale a finalizar.

        Retorna un JSON con:
            - status: "redirect".
            - url: "worker_voucher_1".
            - mensaje: Descripción del resultado.
        """
        # Obtener datos básicos.
        casetero = session.get("worker")
        data = request.json
        identificacion = data.get('identificacion')

        # Obtener horario.
        horario = obtener_horario()

        # Verificar existencia del vale.
        solicitud = vale_existente_estudiante(identificacion)

        # Procesar materiales y datos del casetero.
        materiales =json.loads(solicitud[16])
        caseteroName = casetero[1] + ' ' + casetero[2]
        estudiante = obtenerEstudianteDB(solicitud[1])

        # Actualizar contadores según tipo de vale.
        if solicitud[14] == 'LABORATORIO':
            vales_cantidad(solicitud[14], '0', solicitud[1])
        elif solicitud[14] == 'PROYECTO':
            if estudiante[0] != '0':
                cantidad = int(estudiante[0])
                cantidad = str(cantidad - 1)
            else:
                cantidad = '0'
            vales_cantidad(solicitud[14], cantidad, solicitud[1])

        # Registrar en historial y retornar confirmación.
        registrarVale(casetero[3], identificacion, materiales, horario, solicitud, caseteroName)
        return {"status": "redirect", "url": url_for('worker_voucher_1'), 'mensaje': 'Vale Finalizado'}
    
    @app.route('/casetero/vales/activos/<string:identificacion>', methods = ['GET'])
    @action_required_w  # Decorador que verifica sesión activa.
    def worker_voucher_1_4(identificacion):
        """
        Muestra los detalles de un vale activo para su gestión y edición de materiales.
        
        Permite al casetero:
        - Visualizar los detalles completos de un vale activo.
        - Ver los materiales actualmente asignados.
        - Agregar nuevos materiales disponibles.
        - Eliminar o reportar materiales asignados.
        
        Parametros:
            identificacion: ID único del vale a gestionar.
        """
        casetero = session.get("worker")
        # Recupera los datos del vale específico.
        solicitud = vale_existente_estudiante(identificacion)
        materiales = json.loads(solicitud[16])

        # Obtiene equipos disponibles del laboratorio del casetero.
        equipo = obtenerMaterialCaseteroEditar(casetero[3])
        return render_template('worker_2_1.html', casetero = casetero, solicitud = solicitud, equipo = equipo, materiales =  materiales)
    
    @app.route('/casetero/vales/activos/editado', methods = ['POST'])
    @action_required_w  # Decorador que verifica sesión activa.
    def worker_voucher_1_4_1():
        """
        Procesa la actualización de un vale activo, incluyendo cambios en materiales y observaciones en los materiales.

        Esta ruta maneja:
        - Restablecimiento de materiales anteriores.
        - Actualización de nuevos materiales asignados.
        - Registro de materiales reportados.
        - Actualización del vale en la base de datos.

        Returns:
            JSON: Respuesta con estado de redirección y mensaje de confirmación.
        """
        # Obtener información del casetero desde la sesión.
        casetero = session.get("worker")

        # Procesar datos recibidos.
        data = request.json
        identificacion = data.get('identificacion')

        # Obtener datos actuales del vale.
        solicitud = vale_existente_estudiante(identificacion)
        materiales = json.loads(solicitud[16])

        # Restablecer estado de materiales anteriores.
        materialReportadoReseteado(casetero[3], materiales)

        # Procesar nuevos materiales asignados.
        materiales = data.get('materiales')
        materialReportadoReseteadoOcupado(casetero[3], materiales)

        # Registrar materiales reportados.
        reportados = data.get('reportados')
        materialReportado(casetero[3], reportados)

        # Actualizar el vale con los nuevos materiales.
        editadoVale(identificacion, materiales)
        return {"status": "redirect", "url": url_for('worker_voucher_1'), 'mensaje': 'Vale Actualizado Exitosamente'}
    
    @app.route('/casetero/vales/pendientes', methods = ['GET'])
    @action_required_w  # Decorador que verifica sesión activa.
    def worker_voucher_2():
        """
        Muestra la lista de vales pendientes de aprobación para el laboratorio del casetero,
        junto con los materiales disponibles para asignar.

        Flujo:
            1. Verifica autenticación del casetero.
            2. Obtiene vales pendientes del laboratorio asignado.
            3. Procesa los materiales solicitados en cada vale.
            4. Obtiene equipos disponibles del laboratorio.
            5. Prepara datos para la vista de gestión.
        """
        # Obtener información del casetero desde la sesión.
        casetero = session.get("worker")

        # Obtener vales pendientes para el laboratorio del casetero.
        solicitudes = valesParaCaseteroInfo(casetero[3])

        # Obtener equipos disponibles del laboratorio y agruparlos. 
        equipo = obtenerMaterialCasetero(casetero[3])
        equipo = crearListadeEquipo(equipo)
        return render_template('worker_3.html', casetero = casetero, solicitudes = solicitudes, equipo = equipo)
    
    @app.route('/casetero/vales/pendientes/api/materiales/<vale_id>')
    @action_required_w  # Decorador que verifica sesión activa.
    def worker_voucher_2_api_1(vale_id):
        materiales = materialesValesApi(vale_id)
        materiales = json.loads(materiales[0])
        return jsonify(materiales)
    
    @app.route('/casetero/vales/pendientes/completado', methods = ['POST'])
    @action_required_w  # Decorador que verifica sesión activa.
    def worker_voucher_2_1():
        """
        Procesa la activación de un vale pendiente, asignando materiales y actualizando estados.
        
        Flujo:
            1. Autentica al casetero.
            2. Recibe datos del vale a activar.
            3. Registra fecha/hora de aceptación.
            4. Actualiza estado de materiales y vale.
            5. Retorna confirmación para redirección.
        """
        # Procesar datos de la solicitud.
        casetero = session.get("worker")
        data = request.json
        identificacion = data.get('identificacion')
        materiales = data.get('materiales')
        horario = obtener_horario()

        # Procesar datos de la solicitud.
        materialAsignado(casetero[3], identificacion, materiales, horario)
        return {"status": "redirect", "url": url_for('worker_voucher_2'), 'mensaje': 'Vale Activado Exitosamente'}
    
    @app.route('/casetero/vales/pendientes/cancelado', methods = ['POST'])
    @action_required_w  # Decorador que verifica sesión activa.
    def worker_voucher_2_2():
        """
        Maneja la cancelación de una solicitud de vale pendiente.

        Flujo:
            1. Verifica autenticación del casetero.
            2. Obtiene datos de la solicitud a cancelar.
            3. Realiza validación de existencia.
            4. Procesa según tipo de vale:
                - Laboratorio: Resetea contador.
                - Proyecto: Decrementa contador del estudiante.
            5. Elimina la solicitud.
            6. Retorna estado de la operación.
        """
        # Obtener información del casetero desde sesión.
        casetero = session.get("worker")

        # Procesar datos.
        data = request.json
        identificacion = data.get('identificacion')

        # Verificar existencia de la solicitud.
        solicitud = vale_existente_estudiante(identificacion)
        if solicitud:
            # Obtener datos del estudiante asociado.
            estudiante = obtenerEstudianteDB(solicitud[1])

            # Gestión diferenciada por tipo de vale.
            if solicitud[14] == 'LABORATORIO':
                    vales_cantidad(solicitud[14], '0', solicitud[1])
            elif solicitud[14] == 'PROYECTO':
                    if estudiante[0] != '0':
                        cantidad = int(estudiante[0])
                        cantidad = str(cantidad - 1)
                    else:
                         cantidad = '0'
                    vales_cantidad(solicitud[14], cantidad, solicitud[1])
            # Eliminar la solicitud independientemente del tipo.
            eliminarSolicitudEstudiante(identificacion)
            return {"status": "alerta",'mensaje': 'Solicitud Cancelada'}
        return {"status": "error",'mensaje': 'Solicitud Inexistente'}
    
    @app.route('/casetero/vales/maestros', methods = ['GET'])
    @action_required_w  # Decorador que verifica sesión activa.
    def worker_teacher_1():
        """
        Muestra el listado de vales maestros pendientes de gestión
        en el laboratorio asignado al casetero.

        Flujo:
            1. Autentica al casetero mediante sesión.
            2. Obtiene vales maestros pendientes del laboratorio.
            3. Procesa los materiales solicitados en cada vale.
        """
        # Obtener información del casetero desde la sesión.
        casetero = session.get("worker")

        # Obtener vales maestros pendientes para el laboratorio.
        solicitudes = valesParaCaseteroMaestro(casetero[3])

        # Procesar materiales de cada vale.
        material = {}
        for solicitud in solicitudes:
            k = json.loads(solicitud[16])
            material[solicitud[0]] = k
        return render_template('worker_4.html', casetero = casetero, solicitudes = solicitudes, material = material)
    
    @app.route('/casetero/vales/maestros/finalizar', methods = ['POST'])
    @action_required_w  # Decorador que verifica sesión activa.
    def worker_teacher_1_1():
        """
        Finaliza y registra un vale maestro, actualizando:
            1. El estado de los materiales a 'DISPONIBLE'.
            2. El registro del vale con fecha/hora de finalización.
            3. La información del casetero que realizó la acción.

        Returns:
            JSON: Respuesta con:
                - status: "redirect" .
                - url: Endpoint para redirección.
                - mensaje: Confirmación de la operación.
        """
        # Obtener información del casetero desde sesión.
        casetero = session.get("worker")

        # Procesar datos.
        data = request.json
        identificacion = data.get('identificacion')
        horario = obtener_horario()

        # Recuperar información completa del vale.
        solicitud = vale_existente_estudiante(identificacion)
        materiales =json.loads(solicitud[16])
        caseteroName = casetero[1] + ' ' + casetero[2]

        # Ejecutar el registro completo del vale.
        registrarVale(casetero[3], identificacion, materiales, horario, solicitud, caseteroName)
        return {"status": "redirect", "url": url_for('worker_teacher_1'), 'mensaje': 'Vale Finalizado'}
    
    @app.route('/casetero/vales/maestros/<string:identificacion>', methods = ['GET'])
    @action_required_w  # Decorador que verifica sesión activa.
    def worker_teacher_1_2(identificacion):
        """
        Muestra el detalle de un vale maestro específico para su gestión, incluyendo:
        - Información completa del vale.
        - Materiales actualmente asignados.
        - Equipos disponibles para modificación.
        """
        # Obtener información del casetero desde sesión.
        casetero = session.get("worker")

        # Recuperar información completa del vale maestro.
        solicitud = vale_existente_estudiante(identificacion)
        materiales = json.loads(solicitud[16])

        # Obtener equipos disponibles del laboratorio para posibles modificaciones.
        equipo = obtenerMaterialCaseteroEditar(casetero[3])
        return render_template('worker_4_1.html', casetero = casetero, solicitud = solicitud, equipo = equipo, materiales =  materiales)
    
    @app.route('/casetero/vales/maestros/editado', methods = ['POST'])
    @action_required_w  # Decorador que verifica sesión activa.
    def worker_teacher_1_2_1():
        """
        Procesa la actualización de un vale activo, incluyendo cambios en materiales y observaciones en los materiales.

        Esta ruta maneja:
        - Restablecimiento de materiales anteriores.
        - Actualización de nuevos materiales asignados.
        - Registro de materiales reportados.
        - Actualización del vale en la base de datos.

        Returns:
            JSON: Respuesta con estado de redirección y mensaje de confirmación.
        """
        # Obtener información del casetero desde la sesión.
        casetero = session.get("worker")

        # Procesar datos recibidos.
        data = request.json
        identificacion = data.get('identificacion')

        # Obtener datos actuales del vale.
        solicitud = vale_existente_estudiante(identificacion)
        materiales = json.loads(solicitud[16])

        # Restablecer estado de materiales anteriores.
        materialReportadoReseteado(casetero[3], materiales)
        
        # Procesar nuevos materiales asignados.
        materiales = data.get('materiales')
        materialReportadoReseteadoOcupado(casetero[3], materiales)

        # Registrar materiales reportados.
        reportados = data.get('reportados')
        materialReportado(casetero[3], reportados)

        # Actualizar el vale con los nuevos materiales.
        editadoVale(identificacion, materiales)
        return {"status": "redirect", "url": url_for('worker_teacher_1'), 'mensaje': 'Vale Actualizado Exitosamente'}
    
    @app.route('/casetero/material', methods = ['GET'])
    @action_required_w  # Decorador que verifica sesión activa.
    def worker_materials():
        """
        Muestra el inventario completo de materiales del laboratorio asignado al casetero,
        incluyendo tanto el listado detallado como un resumen por tipo de equipo.

        Flujo:
            1. Verifica autenticación del casetero.
            2. Obtiene datos del inventario del laboratorio asignado.
            3. Organiza la información para visualización.
            4. Renderiza la vista de gestión de materiales.
        """
        casetero = session.get("worker")

        # Obtener datos completos del inventario del laboratorio.
        material, equipo = materialLaboratorio(casetero[3])
        return render_template('worker_5.html', casetero = casetero, material = material, equipo = equipo)
    
    @app.route('/casetero/material/actualizado', methods = ['POST'])
    @action_required_w  # Decorador que verifica sesión activa.
    def worker_materials_1():
        """
        Procesa la actualización de información de materiales o componentes en el inventario del laboratorio.
        Maneja dos flujos distintos:
            1. Para equipos principales.
            2. Para componentes.

        Parámetros:
            identificacion: ID del material a actualizar.
            valores: Lista con los valores a actualizar.

        Returns:
            JSON: Respuesta con:
                - status: "redirect"|"error".
                - url: Endpoint para redirección.
                - mensaje: Descripción del resultado.
        """
        # Obtener información del casetero desde sesión.
        casetero = session.get("worker")

        # Procesar datos.
        data = request.json
        identificacion = data.get('identificacion')
        valores = data.get('valores')

        horario = obtener_horario()
        identi = crear_identificacion_m('UP', horario, casetero[3])

        # Determinar tipo de material por cantidad de campos.
        if len(valores) >= 11:

            # Verificar si ya existe otro material con misma caseta.
            resultado = materialLaboratorioChecar(casetero[3], valores[0], valores[1])

            # Retornar confirmación de actualización.
            if resultado is None:
                materialLaboratorioActualizar(casetero[3], identificacion, valores[0], valores[1], valores[2], valores[3], valores[4], 
                                valores[5], valores[8], valores[9], valores[6], valores[7], valores[10])
            elif str(resultado[0]) == identificacion:
                materialLaboratorioActualizar(casetero[3], identificacion, valores[0], valores[1], valores[2], valores[3], valores[4], 
                                valores[5], valores[8], valores[9], valores[6], valores[7], valores[10])
            else:
                return {"status": "error",'mensaje': 'Este número de caseta ya ha sido asignado a otro material.'}
            registrarModficacionMaterial(identi, valores[0], valores[1], 'EDITADO', horario, casetero[3], casetero[1] + ' ' + casetero[2])
            return {"status": "redirect", "url": url_for('worker_materials'), 'mensaje': 'Material Actualizado'}
        else:
            # Retornar confirmación de actualización.
            componenteLaboratorioModificar(casetero[3], identificacion, valores[2], valores[3], valores[1], valores[6])
            registrarModficacionMaterial(identi, valores[0], 'COMPONENTE', 'EDITADO', horario, casetero[3], casetero[1] + ' ' + casetero[2])
            return {"status": "redirect", "url": url_for('worker_materials'), 'mensaje': 'Material Actualizado'}
        
    @app.route('/casetero/material/eliminado', methods = ['POST'])
    @action_required_w  # Decorador que verifica sesión activa.
    def worker_materials_2():
        """
        Maneja la eliminación de materiales del inventario del laboratorio.

        Flujo:
            1. Verifica autenticación del casetero
            2. Recibe el ID del material a eliminar
            3. Ejecuta la eliminación permanente
            4. Retorna confirmación para redirección
        """
        casetero = session.get("worker")
        data = request.json
        identificacion = data.get('identificacion')

        horario = obtener_horario()
        identi = crear_identificacion_m('DEL', horario, casetero[3])
        valores = materialLaboratorioChecar_m(casetero[3], identificacion)
        if valores[4] == 'S/A':
            caseta = 'COMPONENTE'
        else:
            caseta = valores[4]
        registrarModficacionMaterial(identi, valores[1], caseta, 'ELIMINADO', horario, casetero[3], casetero[1] + ' ' + casetero[2])
        
        componenteLaboratorioBorrar(casetero[3], identificacion)
        return {"status": "redirect", "url": url_for('worker_materials'), 'mensaje': 'Material Eliminado Correctamente'}

    @app.route('/casetero/material/pdf')
    @action_required_w  # Decorador que verifica sesión activa.
    def worker_materials_3():
        """
        Genera y descarga un reporte PDF del inventario completo del laboratorio asignado al casetero.

        Flujo:
            1. Verifica autenticación del usuario.
            2. Genera el PDF con todos los materiales del laboratorio.
            3. Devuelve el archivo como descarga automática.
        """
        casetero = session.get("worker")
        pdf_buffer = generarMaterialesPDF(casetero[3])
        return Response(
            pdf_buffer,
            mimetype='application/pdf',
            headers={"Content-Disposition": f"attachment;filename=materiales({casetero[3]}).pdf"}
        )
    
    @app.route('/casetero/material/csv')
    @action_required_w  # Decorador que verifica sesión activa.
    def worker_materials_4():
        """
        Genera y descarga un reporte CSV del inventario completo del laboratorio asignado al casetero.

        Flujo:
            1. Verifica autenticación del usuario.
            2. Genera el CSV con todos los materiales del laboratorio.
            3. Devuelve el archivo como descarga automática.
        """
        casetero = session.get("worker")
        return Response(
            generarListaMaterialesCSV(casetero[3]),
            mimetype='text/csv',
            headers={"Content-Disposition": f"attachment;filename=materiales({casetero[3]}).csv"}
        )
    
    @app.route('/casetero/material/agregado', methods = ['POST'])
    @action_required_w  # Decorador que verifica sesión activa.
    def worker_materials_5():
        """
        Maneja el registro de nuevos materiales en el inventario del laboratorio, 
        diferenciando entre equipos principales y componentes/consumibles.

        Flujo principal:
            1. Verifica autenticación del casetero
            2. Procesa datos JSON recibidos
            3. Distingue entre:
            - Equipos principales (control individual)
            - Componentes/consumibles (control por cantidad)
            4. Realiza la operación correspondiente:
            - Registro nuevo material
            - Actualización de existencias
            5. Retorna confirmación para redirección

        Parámetros (JSON):
            radio: Tipo de material ('Equipo'|'Componente').
            equipo: Nombre del material.
            marca: Marca del equipo.
            modelo: Modelo específico.
            [Para equipos]:
                caseta: Ubicación física.
                serie: Número de serie.
                inventario: Número de inventario.
                voltaje: Requerimiento eléctrico.
                potencia: Consumo energético.
            [Para componentes]:
                cantidad: Unidades a agregar.

        Returns:
            JSON: Respuesta con estado de redirección y mensaje.
        """
        casetero = session.get("worker")

        # Procesar datos de la solicitud.
        data = request.json
        radio = data.get('radio')
        equipo = data.get('equipo')
        marca = data.get('marca')
        modelo = data.get('modelo')

        horario = obtener_horario()
        identi = crear_identificacion_m('ADD', horario, casetero[3])

        # Procesamiento según tipo de material.
        if radio == 'Equipo':
            numeracion = 'SI'
            caseta = data.get('caseta')
            if caseta == '': caseta = 'S/A'
            serie = data.get('serie')
            if serie == '': serie = 'S/A'
            inventario = data.get('inventario')
            if inventario == '': inventario = 'S/A'
            voltaje = data.get('voltaje')
            if voltaje == '': voltaje = 'S/A'
            potencia = data.get('potencia')
            if potencia == '': potencia = 'S/A'
            if marca == '': marca = 'S/A'
            if modelo == '': modelo = 'S/A'

            # Registrar nuevo equipo.
            registrarModficacionMaterial(identi, equipo, caseta, 'AGREGADO', horario, casetero[3], casetero[1] + ' ' + casetero[2])
            agregarNuevoMaterial(casetero[3], equipo, marca, modelo, numeracion, caseta, serie, inventario, voltaje, potencia)
        elif radio == 'Componente':
            numeracion = 'NO'
            cantidad = data.get('cantidad')

            # Lógica para diferentes combinaciones de marca/modelo.
            if marca == '' and modelo == '':
                material_c = materialLaboratorioVerificarCantidad(casetero[3], equipo, 'S/A', 'S/A')
                if material_c:
                    cantidad = int(cantidad) + material_c[0]
                    materialLaboratorioActualizarCantidad(casetero[3], cantidad, equipo, 'S/A', 'S/A')
                else:
                    # Registrar nuevo equipo.
                    agregarNuevoMaterial(casetero[3], equipo, marca, modelo, numeracion, 'S/A', 'S/A', 'S/A', 'S/A', 'S/A', cantidad)
            elif (marca != '' and modelo != '') or (marca != '' and modelo == '') or (marca == '' and modelo != ''):
                if marca == '': marca = 'S/A'
                if modelo == '': modelo = 'S/A'
                material_c = materialLaboratorioVerificarCantidad(casetero[3], equipo, marca, modelo)
                if material_c:
                    cantidad = int(cantidad) + material_c[0]
                    materialLaboratorioActualizarCantidad(casetero[3], cantidad, equipo, marca, modelo)
                else:
                    # Registrar nuevo equipo.
                    agregarNuevoMaterial(casetero[3], equipo, marca, modelo, numeracion, 'S/A', 'S/A', 'S/A', 'S/A', 'S/A', cantidad)
            registrarModficacionMaterial(identi, equipo, 'COMPONENTE', 'AGREGADO', horario, casetero[3], casetero[1] + ' ' + casetero[2])
        return {"status": "redirect", "url": url_for('worker_materials'), 'mensaje': 'Material Agregado Correctamente'}
    
    @app.route('/casetero/material/registro', methods = ['GET'])
    @action_required_w
    def worker_materials_6():
        casetero = session.get("worker")
        material = materialLaboratorioRegistro(casetero[3])
        return render_template('worker_5_1.html', casetero = casetero, material = material)
    
    @app.route('/casetero/registros', methods = ['GET'])
    @action_required_w  # Decorador que verifica sesión activa.
    def worker_register():
        """
        Muestra el historial completo de registros de préstamos y operaciones para el laboratorio
        asignado al casetero, incluyendo los detalles de materiales involucrados en cada vale.

        Flujo:
            1. Verifica autenticación del casetero.
            2. Obtiene todos los registros históricos del laboratorio.
            3. Procesa los materiales de cada registro.
            4. Renderiza la vista con los datos organizados.
        """
        # Obtener información del casetero desde sesión.
        casetero = session.get("worker")

        # Obtener registros históricos del laboratorio.
        solicitudes = registroLaboratorio(casetero[3])

        # Procesar materiales de cada registro.
        material = {}
        for solicitud in solicitudes:
            k = json.loads(solicitud[18])
            material[solicitud[0]] = k
        return render_template('worker_6.html', casetero = casetero, solicitudes = solicitudes, material = material)
    
    @app.route('/casetero/registros/pdf')
    @action_required_w  # Decorador que verifica sesión activa.
    def worker_register_1():
        """
        Genera y descarga un reporte PDF del historial completo de préstamos del laboratorio asignado al casetero.

        Flujo:
            1. Verifica autenticación del usuario.
            2. Genera el PDF con todos los registros históricos.
            3. Devuelve el archivo como descarga automática con nombre personalizado.
        """
        casetero = session.get("worker")
        pdf_buffer = generarListaPDF(casetero[3])
        return Response(
            pdf_buffer,
            mimetype='application/pdf',
            headers={"Content-Disposition": f"attachment;filename=registro({casetero[3]}).pdf"}
        )
    
    @app.route('/casetero/registros/csv')
    @action_required_w  # Decorador que verifica sesión activa.
    def worker_register_2():
        """
        Genera y descarga un archivo CSV con el historial completo de préstamos del laboratorio asignado al casetero.

        Flujo:
            1. Verifica autenticación del usuario mediante sesión.
            2. Genera el CSV con los registros históricos.
            3. Devuelve el archivo como descarga automática.
        """
        casetero = session.get("worker")
        return Response(
            generarListaCSV(casetero[3]),
            mimetype='text/csv',
            headers={"Content-Disposition": f"attachment;filename=registro({casetero[3]}).csv"}
        )
    
    @app.route('/casetero/registros/nuevo', methods = ['GET'])
    @action_required_w  # Decorador que verifica sesión activa.
    def worker_register_3():
        """
        Muestra el formulario para registrar un nuevo vale de préstamo de materiales, 
        precargando todos los datos necesarios para su gestión.

        Flujo:
            1. Verifica autenticación del casetero.
            2. Obtiene datos maestros, materiales y horario.
            3. Renderiza el formulario con el contexto completo.
        """
        # Obtener información del casetero desde sesión.
        casetero = session.get("worker")

        # Cargar datos necesarios para el formulario.
        maestros = maestros_registrados()
        equipo = obtenerMaterialCaseteroRegistrar(casetero[3])
        horarios = obtener_horario()
        return render_template('worker_6_1.html', casetero = casetero, maestros = maestros, equipo = equipo, fecha = horarios[0])
    
    @app.route('/casetero/registros/nuevo/agregar', methods = ['POST'])
    @action_required_w  # Decorador que verifica sesión activa.
    def worker_register_3_1():
        """
        Procesa el formulario para registrar un nuevo préstamo de materiales en el sistema.

        Flujo:
            1. Verifica autenticación del casetero.
            2. Recibe y valida datos del formulario.
            3. Genera identificador único para el vale.
            4. Verifica existencia del usuario.
            5. Registra la solicitud en la base de datos.
            6. Retorna confirmación o error.

        Parámetros:
            control: Número de control del solicitante.
            materia: Materia/proyecto relacionado.
            grupo: Grupo/clase.
            vale: Tipo de vale (LABORATORIO/PROYECTO/MAESTRO).
            profesor: Profesor responsable.
            alumnos: Cantidad de alumnos.
            laboratorio: Laboratorio destino.
            items: Lista de materiales.
            reporte: Observaciones adicionales.

        Returns:
            JSON: Respuesta con:
                - status: "redirect"|"error".
                - url: Endpoint para redirección.
                - mensaje: Descripción del resultado.
        """
        # Obtener información del casetero desde sesión.
        casetero = session.get("worker")

        # Procesar datos.
        data = request.json
        horarios = obtener_horario()
        ncontrol = data.get('control')
        materia = data.get('materia')
        grupo = data.get('grupo')
        vale = data.get('vale')
        profesor = data.get('profesor')
        alumnos = data.get('alumnos')
        laboratorio = data.get('laboratorio')
        identificacion = crear_identificacion(ncontrol, vale, horarios)
        nombres = obtenerUsuario(vale, ncontrol)

        # Preparar datos para registro.
        if nombres:
            # Registrar en base de datos.
            items = json.dumps(data.get('items'))
            reporte = data.get('reporte')
            solicitud = [ncontrol, nombres[0], nombres[1], materia, grupo, vale, profesor, alumnos, laboratorio, reporte]
            caseteroName = casetero[1] + ' ' + casetero[2]
            registrarSolicitud(identificacion, items, horarios, solicitud, caseteroName)
            return {"status": "redirect", "url": url_for('worker_register'), 'mensaje': 'Registro Agregado Correctamente'}
        return {"status": "error",'mensaje': 'Usuario Inexistente'}

    @app.route('/casetero/perfil', methods = ['GET'])
    @action_required_w  # Decorador que verifica sesión activa.
    def worker_profile():
        """
        Muestra la página de perfil del casetero con su información personal y laboral.
        """
        casetero = session.get("worker")
        return render_template('worker_7.html', casetero = casetero)