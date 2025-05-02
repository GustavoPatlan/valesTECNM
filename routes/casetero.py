from flask import redirect, render_template, request, session, url_for, Response
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

def rutasDeTrabajador(app, socketio):
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
        casetero = session.get("worker")
        solicitud = vale_existente_estudiante(identificacion)
        materiales = json.loads(solicitud[16])
        equipo = obtenerMaterialCaseteroEditar(casetero[3])
        return render_template('worker_2_1.html', casetero = casetero, solicitud = solicitud, equipo = equipo, materiales =  materiales)
    
    @app.route('/casetero/vales/activos/editado', methods = ['POST'])
    @action_required_w
    def worker_voucher_1_4_1():
        casetero = session.get("worker")
        data = request.json
        identificacion = data.get('identificacion')
        materiales = data.get('materiales')
        reportados = data.get('reportados')
        materialReportado(casetero[3], reportados)
        editadoVale(identificacion, materiales)
        return {"status": "redirect", "url": url_for('worker_voucher_1'), 'mensaje': 'Vale Actualizado Exitosamente'}
    
    @app.route('/casetero/vales/pendientes', methods = ['GET'])
    @action_required_w
    def worker_voucher_2():
        casetero = session.get("worker")
        solicitudes = valesParaCaseteroInfo(casetero[3])
        material = {}
        for solicitud in solicitudes:
            k = json.loads(solicitud[16])
            material[solicitud[0]] = k
        equipo = obtenerMaterialCasetero(casetero[3])
        equipo = crearListadeEquipo(equipo)
        return render_template('worker_3.html', casetero = casetero, solicitudes = solicitudes, material = material,
                               equipo = equipo)
    
    @app.route('/casetero/vales/pendientes/completado', methods = ['POST'])
    @action_required_w
    def worker_voucher_2_1():
        casetero = session.get("worker")
        data = request.json
        identificacion = data.get('identificacion')
        materiales = data.get('materiales')
        horario = obtener_horario()
        materialAsignado(casetero[3], identificacion, materiales, horario)
        return {"status": "redirect", "url": url_for('worker_voucher_2'), 'mensaje': 'Vale Activado Exitosamente'}
    
    @app.route('/casetero/vales/pendientes/cancelado', methods = ['POST'])
    @action_required_w
    def worker_voucher_2_2():
        casetero = session.get("worker")
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
    
    @app.route('/casetero/vales/maestros', methods = ['GET'])
    @action_required_w
    def worker_teacher_1():
        casetero = session.get("worker")
        solicitudes = valesParaCaseteroMaestro(casetero[3])
        material = {}
        for solicitud in solicitudes:
            k = json.loads(solicitud[16])
            material[solicitud[0]] = k
        return render_template('worker_4.html', casetero = casetero, solicitudes = solicitudes, material = material)
    
    @app.route('/casetero/vales/maestros/finalizar', methods = ['POST'])
    @action_required_w
    def worker_teacher_1_1():
        casetero = session.get("worker")
        data = request.json
        identificacion = data.get('identificacion')
        horario = obtener_horario()
        solicitud = vale_existente_estudiante(identificacion)
        materiales =json.loads(solicitud[16])
        caseteroName = casetero[1] + ' ' + casetero[2]
        registrarVale(casetero[3], identificacion, materiales, horario, solicitud, caseteroName)
        return {"status": "redirect", "url": url_for('worker_teacher_1'), 'mensaje': 'Vale Finalizado'}
    
    @app.route('/casetero/vales/maestros/<string:identificacion>', methods = ['GET'])
    @action_required_w
    def worker_teacher_1_2(identificacion):
        casetero = session.get("worker")
        solicitud = vale_existente_estudiante(identificacion)
        materiales = json.loads(solicitud[16])
        equipo = obtenerMaterialCaseteroEditar(casetero[3])
        return render_template('worker_4_1.html', casetero = casetero, solicitud = solicitud, equipo = equipo, materiales =  materiales)
    
    @app.route('/casetero/vales/maestros/editado', methods = ['POST'])
    @action_required_w
    def worker_teacher_1_2_1():
        casetero = session.get("worker")
        data = request.json
        identificacion = data.get('identificacion')
        materiales = data.get('materiales')
        reportados = data.get('reportados')
        materialReportado(casetero[3], reportados)
        editadoVale(identificacion, materiales)
        return {"status": "redirect", "url": url_for('worker_teacher_1'), 'mensaje': 'Vale Actualizado Exitosamente'}
    
    @app.route('/casetero/material', methods = ['GET'])
    @action_required_w
    def worker_materials():
        casetero = session.get("worker")
        material, equipo = materialLaboratorio(casetero[3])
        return render_template('worker_5.html', casetero = casetero, material = material, equipo = equipo)
    
    @app.route('/casetero/material/actualizado', methods = ['POST'])
    @action_required_w
    def worker_materials_1():
        casetero = session.get("worker")
        data = request.json
        identificacion = data.get('identificacion')
        valores = data.get('valores')
        if len(valores) >= 11:
            resultado = materialLaboratorioChecar(casetero[3], valores[0], valores[1])
            if resultado is None:
                materialLaboratorioActualizar(casetero[3], identificacion, valores[0], valores[1], valores[2], valores[3], valores[4], 
                                valores[5], valores[8], valores[9], valores[6], valores[7], valores[10])
            elif str(resultado[0]) == identificacion:
                materialLaboratorioActualizar(casetero[3], identificacion, valores[0], valores[1], valores[2], valores[3], valores[4], 
                                valores[5], valores[8], valores[9], valores[6], valores[7], valores[10])
            else:
                return {"status": "error",'mensaje': 'Este número de caseta ya ha sido asignado a otro material.'}
            return {"status": "redirect", "url": url_for('worker_materials'), 'mensaje': 'Material Actualizado'}
        else:
            componenteLaboratorioModificar(casetero[3], identificacion, valores[2], valores[3], valores[1], valores[6])
            return {"status": "redirect", "url": url_for('worker_materials'), 'mensaje': 'Material Actualizado'}
        
    @app.route('/casetero/material/eliminado', methods = ['POST'])
    @action_required_w
    def worker_materials_2():
        casetero = session.get("worker")
        data = request.json
        identificacion = data.get('identificacion')
        componenteLaboratorioBorrar(casetero[3], identificacion)
        return {"status": "redirect", "url": url_for('worker_materials'), 'mensaje': 'Material Eliminado Correctamente'}

    @app.route('/casetero/material/pdf')
    @action_required_w
    def worker_materials_3():
        casetero = session.get("worker")
        pdf_buffer = generarMaterialesPDF(casetero[3])
        return Response(
            pdf_buffer,
            mimetype='application/pdf',
            headers={"Content-Disposition": f"attachment;filename=materiales({casetero[3]}).pdf"}
        )
    
    @app.route('/casetero/material/csv')
    @action_required_w
    def worker_materials_4():
        casetero = session.get("worker")
        return Response(
            generarListaMaterialesCSV(casetero[3]),
            mimetype='text/csv',
            headers={"Content-Disposition": f"attachment;filename=materiales({casetero[3]}).csv"}
        )
    
    @app.route('/casetero/material/agregado', methods = ['POST'])
    @action_required_w
    def worker_materials_5():
        casetero = session.get("worker")
        data = request.json
        radio = data.get('radio')
        equipo = data.get('equipo')
        marca = data.get('marca')
        modelo = data.get('modelo')
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
            agregarNuevoMaterial(casetero[3], equipo, marca, modelo, numeracion, caseta, serie, inventario, voltaje, potencia)
        elif radio == 'Componente':
            numeracion = 'NO'
            cantidad = data.get('cantidad')
            if marca == '' and modelo == '':
                material_c = materialLaboratorioVerificarCantidad(casetero[3], equipo, 'S/A', 'S/A')
                cantidad = int(cantidad) + material_c[0]
                materialLaboratorioActualizarCantidad(casetero[3], cantidad, equipo, 'S/A', 'S/A')
            elif (marca != '' and modelo != '') or (marca != '' and modelo == '') or (marca == ''and modelo != ''):
                if marca == '': marca = 'S/A'
                if modelo == '': modelo = 'S/A'
                material_c = materialLaboratorioVerificarCantidad(casetero[3], equipo, marca, modelo)
                if material_c:
                    cantidad = int(cantidad) + material_c[0]
                    materialLaboratorioActualizarCantidad(casetero[3], cantidad, equipo, marca, modelo)
                else:
                    agregarNuevoMaterial(casetero[3], equipo, marca, modelo, numeracion, 'S/A', 'S/A', 'S/A', 'S/A', 'S/A', cantidad)
        return {"status": "redirect", "url": url_for('worker_materials'), 'mensaje': 'Material Agregado Correctamente'}
    
    @app.route('/casetero/registros', methods = ['GET'])
    @action_required_w
    def worker_register():
        casetero = session.get("worker")
        solicitudes = registroLaboratorio(casetero[3])
        material = {}
        for solicitud in solicitudes:
            k = json.loads(solicitud[18])
            material[solicitud[0]] = k
        return render_template('worker_6.html', casetero = casetero, solicitudes = solicitudes, material = material)
    
    @app.route('/casetero/registros/pdf')
    @action_required_w
    def worker_register_1():
        casetero = session.get("worker")
        pdf_buffer = generarListaPDF(casetero[3])
        return Response(
            pdf_buffer,
            mimetype='application/pdf',
            headers={"Content-Disposition": f"attachment;filename=registro({casetero[3]}).pdf"}
        )
    
    @app.route('/casetero/registros/csv')
    @action_required_w
    def worker_register_2():
        casetero = session.get("worker")
        return Response(
            generarListaCSV(casetero[3]),
            mimetype='text/csv',
            headers={"Content-Disposition": f"attachment;filename=registro({casetero[3]}).csv"}
        )
    
    @app.route('/casetero/registros/nuevo', methods = ['GET'])
    @action_required_w
    def worker_register_3():
        casetero = session.get("worker")
        maestros = maestros_registrados()
        equipo = obtenerMaterialCaseteroRegistrar(casetero[3])
        horarios = obtener_horario()
        return render_template('worker_6_1.html', casetero = casetero, maestros = maestros, equipo = equipo, fecha = horarios[0])
    
    @app.route('/casetero/registros/nuevo/agregar', methods = ['POST'])
    @action_required_w
    def worker_register_3_1():
        casetero = session.get("worker")
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
        if nombres:
            items = json.dumps(data.get('items'))
            reporte = data.get('reporte')
            solicitud = [ncontrol, nombres[0], nombres[1], materia, grupo, vale, profesor, alumnos, laboratorio, reporte]
            caseteroName = casetero[1] + ' ' + casetero[2]
            registrarSolicitud(identificacion, items, horarios, solicitud, caseteroName)
            return {"status": "redirect", "url": url_for('worker_register'), 'mensaje': 'Registro Agregado Correctamente'}
        return {"status": "error",'mensaje': 'Usuario Inexistente'}

    @app.route('/casetero/perfil', methods = ['GET'])
    @action_required_w
    def worker_profile():
        casetero = session.get("worker")
        return render_template('worker_7.html', casetero = casetero)