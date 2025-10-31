from config.database import *
import json

lab_conditions = {
        'Y1-Y2': "laboratory = 'Y1' OR laboratory = 'Y2'",
        'Y6-Y7': "laboratory = 'Y6' OR laboratory = 'Y7'",
        'Y8': "laboratory = 'Y8'"
    }

lab_material = {
        'Y1-Y2': "labpotencia",
        'Y6-Y7': "labelectronica",
        'Y8': "labthird"
    }

def valesParaCasetero(laboratorio):
    """
    Obtiene estadísticas de vales asociados a un laboratorio, clasificados por estado.

    Parámetros:
        laboratorio: Nombre del laboratorio.

    Consulta SQL:
        Realiza un conteo de vales agrupados en tres categorías:
        1. Vales ACTIVOS.
        2. Vales EN ESPERA.
        3. Vales DE MAESTROS.

    Resultado:
        Diccionario con tres claves:
            - "activo": Cantidad de vales activos.
            - "espera": Cantidad de vales en espera.
            - "sin": Cantidad de vales activos de maestros.
    """
    condition = lab_conditions.get(laboratorio)
    sql = f"""
        SELECT 
            COUNT(*) AS total,
            SUM(CASE WHEN estado = 'ACTIVO' AND (tipo_vale = 'LABORATORIO' OR tipo_vale = 'PROYECTO') THEN 1 ELSE 0 END) AS total_activo,
            SUM(CASE WHEN estado = 'EN ESPERA' THEN 1 ELSE 0 END) AS total_en_espera,
            SUM(CASE WHEN tipo_vale = 'MAESTRO' THEN 1 ELSE 0 END) AS total_maestro
        FROM solicitud
        WHERE {condition}
    """
    resultado = obtenerDatosDB(sql)

    # Procesa los resultados (convirtiendo None a 0).
    respuesta_1, respuesta_2, respuesta_3 = [
    valor if valor is not None else 0
    for valor in resultado[1:4]
    ]

    return {
        "activo": respuesta_1,
        "espera": respuesta_2,
        "sin": respuesta_3
    }

def valesParaCaseteroInfo(laboratorio):
    """
    Obtiene todos los vales en estado 'EN ESPERA' para un laboratorio específico.
    """
    condition = lab_conditions.get(laboratorio)
    sql = f"""SELECT id_ncontrol, ncontrol, hora_solicitud, fecha_solicitud, name, lastname, teacher, topic, grupo, number_group,
    laboratory, estado, tipo_vale FROM solicitud WHERE estado = 'EN ESPERA' AND ({condition})"""
    resultado = obtenerDatosDB_Varios(sql)
    return resultado

def materialesValesApi(ide):
    sql = "SELECT material FROM solicitud WHERE id_ncontrol LIKE %s"
    data = (f"%{ide}%",)
    resultado = obtenerDatosDB(sql, data)
    return resultado

def valesParaCaseteroActivo(laboratorio):
    """
    Obtiene todas las solicitudes de vales activos de los estudiantes en un laboratorio en específico.

    Parámetros:
        laboratorio: Nombre del laboratorio.

    Retorno:
        Lista de tuplas con todos los campos de las solicitudes, donde cada tupla contiene:
              - Todos los campos de la tabla 'solicitud' en el orden original.
              - Lista vacía si no hay solicitudes pendientes.
    """
    condition = lab_conditions.get(laboratorio)
    sql = f"SELECT * FROM solicitud WHERE estado = 'ACTIVO' AND ({condition}) AND (tipo_vale = 'LABORATORIO' OR tipo_vale = 'PROYECTO')"
    resultado = obtenerDatosDB_Varios(sql)
    return resultado

def valesParaCaseteroMaestro(laboratorio):
    """
    Obtiene todos los vales de tipo 'MAESTRO' activos para un laboratorio específico.

    Esta función consulta las solicitudes de vales maestros que están 
    asociadas al laboratorio del casetero, para su posterior gestión.
    """
    condition = lab_conditions.get(laboratorio)
    sql = f"SELECT * FROM solicitud WHERE tipo_vale = 'MAESTRO' AND ({condition})"
    resultado = obtenerDatosDB_Varios(sql)
    return resultado

def obtenerMaterialCasetero(laboratorio):
    """
    Obtiene la lista de materiales disponibles y numerados de un laboratorio específico
    para ser gestionados y asignados por el casetero.
    """
    condition = lab_material.get(laboratorio)
    sql = f"SELECT EQUIPO, N_CASETA FROM {condition} WHERE NUMERACION = 'SI' AND disponibilidad = 'DISPONIBLE'"
    resultado = obtenerDatosDB_Varios(sql)
    return resultado

def materialAsignado(laboratorio, identificacion, materiales, horario):
    """
    Gestiona la asignación de materiales para un vale, actualizando:
    1. El estado de los materiales a 'OCUPADO' en el inventario.
    2. La información del vale en la tabla de solicitudes.

    Parámetros:
        laboratorio: Nombre del laboratorio donde se asignan los materiales.
        identificacion: ID único del vale a actualizar.
        materiales: Lista de materiales a asignar.
        horario: Tupla con fecha y hora.

    Flujo:
        1. Actualiza el estado de cada material a 'OCUPADO' en el inventario.
        2. Actualiza el vale con:
           - Materiales asignados.
           - Fecha/hora de aceptación.
           - Estado 'ACTIVO'.
    """
    condition = lab_material.get(laboratorio)
    # Actualizar estado de materiales en el inventario del laboratorio.
    sql = f"UPDATE {condition} SET DISPONIBILIDAD = 'OCUPADO' WHERE EQUIPO = %s AND N_CASETA = %s AND NUMERACION = 'SI'"
    data = (materiales,)
    agregarDatosDB_Individual_for(sql, data)
    material = json.dumps(materiales)
    # Actualizar información del vale en la tabla de solicitudes.
    sql = "UPDATE solicitud SET material = %s, hora_aceptacion = %s, fecha_aceptacion = %s, estado = 'ACTIVO' WHERE id_ncontrol = %s"
    data = (material, horario[1], horario[0], identificacion,)
    agregarDatosDB_Individual(sql, data)

def vale_existente_estudiante(identificacion):
    """
    Verifica la existencia de solicitudes de vale asociadas a un identificador específico.

    Parámetros:
        identificacion: Cadena de identificación o fragmento a buscar en los vales.

    Retorno:
        Lista con los campos de la solicitud coincidente:
            - Lista vacía si no se encuentran coincidencias.
    """
    sql = "SELECT * FROM solicitud WHERE id_ncontrol LIKE %s"
    data = (f"%{identificacion}%",)
    resultado = obtenerDatosDB(sql, data)
    return resultado

def obtenerEstudianteDB(ncontrol):
    """
    Obtiene el estado de proyecto(s) de un estudiante.

    Parámetros:
        ncontrol: Número de control del estudiante.

    Retorno:
        Resultado de la consulta con el campo 'proyecto' o None si no existe
    """
    sql = "SELECT proyecto FROM usuarios WHERE ncontrol = %s"
    data = (ncontrol,)
    resultado = obtenerDatosDB(sql, data)
    return resultado

def vales_cantidad(vale, cantidad, ncontrol):
    """
    Actualiza el contador de vales utilizados por un estudiante, diferenciando entre
    vales de PROYECTO y vales regulares de LABORATORIO.

    Parámetros:
        vale: Tipo de vale.
        cantidad: Nuevo valor a establecer en el contador correspondiente.
        ncontrol: Número de control del estudiante a actualizar.
    """
    if vale == 'PROYECTO':
        sql = "UPDATE usuarios SET proyecto = %s WHERE ncontrol = %s"
    else:
        sql = "UPDATE usuarios SET laboratorio = %s WHERE ncontrol = %s"
    data = (cantidad, ncontrol,)
    agregarDatosDB_Individual(sql, data)

def eliminarSolicitudEstudiante(identificacion):
    """
    Elimina una solicitud de vale de la base de datos mediante su identificador único.

    Parámetros:
        identificacion: Número de control o ID único de la solicitud a eliminar.
    """
    sql = "DELETE FROM solicitud WHERE id_ncontrol = %s"
    data = (identificacion,)
    agregarDatosDB_Individual(sql, data)

def reportarVale(identificacion, reporte='N/A'):
    """
    Actualiza el campo de reporte de una solicitud de vale.

    Parámetros:
        identificacion: ID completo del vale a actualizar.
        reporte: Texto del reporte a asignar, por defecto N/A.
    """
    sql = "UPDATE solicitud SET reporte = %s WHERE id_ncontrol = %s"
    data = (reporte, identificacion,)
    agregarDatosDB_Individual(sql, data)

def registrarVale(laboratorio, identificacion, materiales, horario, solicitud, casetero):
    """
    Registra un vale de préstamo de material en el sistema, actualizando el estado del material,
    creando un nuevo registro y eliminando la solicitud correspondiente.
    
    Parámetros:
        laboratorio: Laboratorio donde se realiza el préstamo.
        identificacion: Identificación del préstamo/solicitud.
        materiales: Materiales prestados.
        horario: Tupla con fecha y hora de finalización.
        solicitud: Datos completos de la solicitud.
        casetero: Responsable que autoriza el préstamo.
    """
    condition = lab_material.get(laboratorio)
    # Actualiza el estado del material a DISPONIBLE en el inventario del laboratorio.
    sql = f"UPDATE {condition} SET DISPONIBILIDAD = 'DISPONIBLE' WHERE EQUIPO = %s AND N_CASETA = %s AND NUMERACION = 'SI'"
    data = (materiales,)

    # Inserta un nuevo registro del vale en la base de datos.
    agregarDatosDB_Individual_for(sql, data)
    sql = '''INSERT INTO registro
    (id_registro, ncontrol, hora_solicitud, fecha_solicitud, hora_aceptacion, fecha_aceptacion, 
    hora_final, fecha_final, name, lastname, teacher, casetero, topic, grupo, number_group, laboratory, 
    tipo_vale, reporte, i_material) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
    data = (
        solicitud[0], solicitud[1], solicitud[2], solicitud[3], solicitud[4], solicitud[5],
        horario[1], horario[0], solicitud[6], solicitud[7], solicitud[8],
        casetero, solicitud[9], solicitud[10], solicitud[11],
        solicitud[12], solicitud[14], solicitud[15], solicitud[16],
    )
    agregarDatosDB_Individual(sql, data)

    # Elimina la solicitud procesada de la tabla de solicitudes.
    sql = "DELETE FROM solicitud WHERE id_ncontrol = %s"
    data = (identificacion,)
    agregarDatosDB_Individual(sql, data)

def registroLaboratorio(laboratorio):
    """
    Obtiene todos los registros de vales históricos para un laboratorio específico, ordenados por fecha de finalización.

    Esta función consulta la tabla 'registro' para obtener el historial completo de préstamos
    y operaciones realizadas en el laboratorio especificado.
    """
    condition = lab_conditions.get(laboratorio)
    sql = f"SELECT * FROM registro WHERE ({condition}) ORDER BY fecha_final ASC"
    resultado = obtenerDatosDB_Varios(sql)
    return resultado

def materialLaboratorio(laboratorio):
    """
    Obtiene información detallada y categorizada de los materiales de un laboratorio específico.
    """
    condition = lab_material.get(laboratorio)
    # Consulta 1: Obtiene todos los materiales con ordenamiento específico.
    sql = f"SELECT * FROM ({condition}) ORDER BY NUMERACION DESC, EQUIPO, N_CASETA ASC"
    resultado_1 = obtenerDatosDB_Varios(sql)

    # Consulta 2: Obtiene equipos únicos con su estado de numeración.
    sql = f"SELECT DISTINCT EQUIPO, NUMERACION FROM {condition}"
    resultado_2 = obtenerDatosDB_Varios(sql)
    return resultado_1, resultado_2

def materialLaboratorioRegistro(laboratorio):
    sql = f"SELECT * FROM materiales WHERE laboratorio = '{laboratorio}' ORDER BY fecha ASC, hora ASC"
    resultado = obtenerDatosDB_Varios(sql)
    return resultado

def registrarModficacionMaterial(identi, material, caseta, accion, horario, laboratorio, responsable):
    sql = '''INSERT INTO materiales
    (id_registro, material, caseta, accion, fecha, hora, laboratorio, responsable) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''
    data = (identi, material, caseta, accion, horario[0], horario[1], laboratorio, responsable,)
    agregarDatosDB_Individual(sql, data)

def materialLaboratorioChecar_m(laboratorio, identificacion):
    condition = lab_material.get(laboratorio)
    sql = f"SELECT * FROM {condition} WHERE id = %s"
    data = (identificacion,)
    resultado = obtenerDatosDB(sql, data)
    return resultado

def materialLaboratorioChecar(laboratorio, equipo, caseta):
    """
    Verifica la existencia de un material específico en el inventario de un laboratorio.

    Esta función es útil para validar si un equipo concreto existe en una caseta específica
    antes de realizar operaciones como préstamos, devoluciones o actualizaciones.
    """
    condition = lab_material.get(laboratorio)
    sql = f"SELECT id FROM {condition} WHERE EQUIPO = %s AND N_CASETA = %s"
    data = (equipo, caseta,)
    resultado = obtenerDatosDB(sql, data)
    return resultado

def materialLaboratorioActualizar(laboratorio, identificacion, equipo, caseta, marca, modelo, serie, 
                           inventario, condicion, disponibilidad, voltaje = 'S/A', potencia = 'S/A', observaciones=''):
    """
    Actualiza toda la información registrada de un material específico en el inventario de un laboratorio.

    Parámetros:
        laboratorio: Nombre del laboratorio donde se encuentra el material.
        identificacion: ID único del material a actualizar.
        equipo: Nombre/tipo del equipo.
        caseta: Número/ubicación de la caseta.
        marca: Marca del equipo.
        modelo: Modelo del equipo.
        serie: Número de serie del fabricante.
        inventario: Número de inventario institucional.
        condicion: Estado físico del equipo.
        disponibilidad: Estado operativo.
        voltaje: Requerimiento eléctrico (default 'S/A').
        potencia: Consumo energético (default 'S/A').
        observaciones: Notas adicionales (default '').
    """
    condition = lab_material.get(laboratorio)
    sql = f"""UPDATE {condition} 
            SET EQUIPO = %s, N_CASETA = %s, MARCA = %s, MODELO = %s, N_SERIE = %s, N_INVENTARIO = %s, 
            VOLTAJE = %s, POTENCIA = %s, CONDICION = %s, DISPONIBILIDAD = %s, OBSERVACIONES = %s WHERE id = %s"""
    data = (equipo, caseta, marca, modelo, serie, inventario, voltaje, potencia, condicion, disponibilidad, observaciones, identificacion,)
    agregarDatosDB_Individual(sql, data)

def componenteLaboratorioModificar(laboratorio, identificacion, marca, modelo, cantidad, observaciones=''):
    """
    Actualiza la información de un componente existente en el inventario de un laboratorio.

    Esta función permite modificar los datos básicos de un componente sin afectar su identificador único,
    ideal para actualizaciones de características o ajustes de inventario.

    Parámetros:
        laboratorio: Nombre del laboratorio donde se encuentra el componente.
        identificacion: ID único del componente en la base de datos.
        marca: Nueva marca del componente.
        modelo: Nuevo modelo del componente.
        cantidad: Nueva cantidad disponible en inventario.
        observaciones: Notas adicionales sobre el componente (default: '').
    """
    condition = lab_material.get(laboratorio)
    sql = f"""
        UPDATE {condition}
        SET MARCA = %s, MODELO = %s, CANTIDAD = %s, OBSERVACIONES = %s
        WHERE id = %s
    """
    data = (marca, modelo, cantidad, observaciones, identificacion,)
    agregarDatosDB_Individual(sql, data)

def componenteLaboratorioBorrar(laboratorio, identificacion):
    """
    Elimina permanentemente un componente del inventario de un laboratorio específico.

    Esta función realiza una eliminación física en la base de datos y debe usarse con precaución.
    Ideal para componentes obsoletos o dados de baja definitiva.

    Parámetros:
        laboratorio: Nombre del laboratorio donde se encuentra el componente.
        identificacion: ID único del componente a eliminar.
    """
    condition = lab_material.get(laboratorio)
    sql = f"DELETE FROM {condition} WHERE id = %s"
    data = (identificacion,)
    agregarDatosDB_Individual(sql, data)

def agregarNuevoMaterial(laboratorio, equipo, marca, modelo, numeracion, caseta, serie, inventario, voltaje, potencia, cantidad = 1):
    """
    Registra un nuevo material en el inventario de un laboratorio específico con valores por defecto seguros.

    Parámetros:
        laboratorio: Nombre del laboratorio destino.
        equipo: Material.
        marca: Marca/fabricante del equipo.
        modelo: Modelo específico.
        numeracion: 'SI' o 'NO' indica si requiere control numérico.
        caseta: Ubicación física.
        serie: Número de serie del fabricante.
        inventario: Número de inventario institucional.
        voltaje: Requerimiento eléctrico.
        potencia: Consumo energético.
        cantidad: Unidades existentes (default 1).
    """
    condition = lab_material.get(laboratorio)
    sql = f'''INSERT INTO {condition}
    (EQUIPO, MARCA, MODELO, N_CASETA, N_SERIE, N_INVENTARIO, 
    VOLTAJE, POTENCIA, CANTIDAD, CONDICION, DISPONIBILIDAD, NUMERACION, OBSERVACIONES) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
    data = (equipo, marca, modelo, caseta, serie, inventario, voltaje, potencia, cantidad, 'OK', 'DISPONIBLE', numeracion, 'OK')
    agregarDatosDB_Individual(sql, data)

def materialLaboratorioVerificarCantidad(laboratorio, equipo, marca, modelo):
    """
    Verifica la cantidad disponible de un material no numerado en el inventario del laboratorio.

    Esta función es útil para componentes que no requieren control individual (NUMERACION = 'NO'),
    como consumibles o materiales genéricos, donde solo interesa la cantidad disponible.
    """
    condition = lab_material.get(laboratorio)
    sql = f"SELECT CANTIDAD FROM {condition} WHERE EQUIPO = %s AND MARCA = %s AND MODELO = %s AND NUMERACION = 'NO'"
    data = (equipo, marca, modelo,)
    resultado = obtenerDatosDB(sql, data)
    return resultado

def materialLaboratorioActualizarCantidad(laboratorio, cantidad, equipo, marca, modelo):
    """
    Actualiza la cantidad disponible de un material no numerado en el inventario del laboratorio.

    Esta función está diseñada específicamente para materiales que no requieren control individual
    (NUMERACION = 'NO'), como consumibles o reactivos, donde solo se manejan cantidades globales.

    Parámetros:
        laboratorio: Nombre del laboratorio donde se actualizará el material.
        cantidad: Nueva cantidad disponible a registrar.
        equipo: Tipo de material/equipo a actualizar.
        marca: Marca específica del material.
        modelo: Modelo específico del material.
    """
    condition = lab_material.get(laboratorio)
    sql = f"""UPDATE {condition} SET CANTIDAD = %s WHERE EQUIPO = %s AND MARCA = %s AND MODELO = %s AND NUMERACION = 'NO'"""
    data = (cantidad, equipo, marca, modelo,)
    agregarDatosDB_Individual(sql, data)

def obtenerMaterialCaseteroEditar(laboratorio):
    """
    Obtiene la lista de materiales disponibles de un laboratorio específico.
    
    Parámetros:
        laboratorio: Nombre del laboratorio del cual se obtendrán los materiales.
        
    Retorna:
        Lista de tuplas con información de los materiales disponibles (EQUIPO, N_CASETA, NUMERACION).
    """
    condition = lab_material.get(laboratorio)
    sql = f"SELECT EQUIPO, N_CASETA, NUMERACION FROM {condition} WHERE disponibilidad = 'DISPONIBLE'"
    resultado = obtenerDatosDB_Varios(sql)
    return resultado

def obtenerMaterialCaseteroRegistrar(laboratorio):
    """
    Obtiene la lista de materiales disponibles en un laboratorio específico para procesos de registro.
    """
    condition = lab_material.get(laboratorio)
    sql = f"SELECT EQUIPO, N_CASETA, NUMERACION FROM {condition}"
    resultado = obtenerDatosDB_Varios(sql)
    return resultado

def materialReportadoReseteado(laboratorio, materiales):
    """
    Restablece el estado de cada material en una lista a 'DISPONIBLE' en el inventario del laboratorio.

    Parámetros:
        laboratorio: Nombre del laboratorio donde se encuentra el material.
        materiales: Lista con los materiales a actualizar.
    """
    condition = lab_material.get(laboratorio)
    sql = f"UPDATE {condition} SET DISPONIBILIDAD = 'DISPONIBLE' WHERE EQUIPO = %s AND N_CASETA = %s"
    data = (materiales,)
    agregarDatosDB_Individual_resetear(sql, data)

def materialReportadoReseteadoOcupado(laboratorio, materiales):
    """
    Restablece el estado de cada material en una lista a 'OCUPADO' en el inventario del laboratorio.

    Parámetros:
        laboratorio: Nombre del laboratorio donde se encuentra el material.
        materiales: Lista con los materiales a actualizar.
    """
    condition = lab_material.get(laboratorio)
    sql = f"UPDATE {condition} SET DISPONIBILIDAD = 'OCUPADO' WHERE EQUIPO = %s AND N_CASETA = %s AND NUMERACION = 'SI'"
    data = (materiales,)
    agregarDatosDB_Individual_resetear_ocupado(sql, data)

def materialReportado(laboratorio, materiales):
    """
    Agrega observaciones a cada material en una lista en el inventario del laboratorio.

    Parámetros:
        laboratorio: Nombre del laboratorio donde se encuentra el material.
        materiales: Lista con los materiales a actualizar.
    """
    condition = lab_material.get(laboratorio)
    sql = f"UPDATE {condition} SET OBSERVACIONES = %s, DISPONIBILIDAD = %s WHERE EQUIPO = %s AND N_CASETA = %s"
    data = (materiales,)
    agregarDatosDB_Individual_reporte(sql, data)

def editadoVale(identificacion, materiales):
    """
    Actualiza los materiales asignados a un vale existente en la base de datos.

    Parámetros:
        identificacion: ID único del vale a modificar.
        materiales: Lista de materiales actualizados para asignar al vale.
    """
    materiales = json.dumps(materiales)
    sql = "UPDATE solicitud SET material = %s WHERE id_ncontrol = %s"
    data = (materiales, identificacion,)
    agregarDatosDB_Individual(sql, data)

def maestros_registrados():
    """
    Obtiene la lista completa de maestros registrados en el sistema, ordenados alfabéticamente por nombre.
    """
    sql = "SELECT nombres, apellidos FROM maestros ORDER BY nombres"
    resultado = obtenerDatosDB_Varios(sql)
    return resultado

def obtenerUsuario(vale, ncontrol):
    """
    Obtiene el nombre completo de un usuario (maestro o estudiante) según el tipo de vale y su número de control.
    """
    if vale == 'MAESTRO':
        lada = 'maestros'
        tipo = 'id'
    else:
        lada = 'usuarios'
        tipo = 'ncontrol'
    sql = f"SELECT nombres, apellidos FROM {lada} WHERE {tipo} = %s"
    data = (ncontrol,)
    resultado = obtenerDatosDB(sql, data)
    return resultado

def registrarSolicitud(identificacion, materiales, horario, solicitud, casetero):
    """
    Registra una nueva solicitud de préstamo en la base de datos con todos los detalles necesarios.

    Parámetros:
        identificacion: ID único generado para el vale.
        materiales: Lista de materiales.
        horario: Tupla con fecha y hora.
        solicitud: Lista con datos del solicitante en este orden:
                        [ncontrol, nombre, apellido, tema, grupo, tipo_vale, profesor, num_grupo, laboratorio, reporte]
        casetero: Nombre del casetero que registra la solicitud.
    """
    sql = '''INSERT INTO registro
    (id_registro, ncontrol, hora_solicitud, fecha_solicitud, hora_aceptacion, fecha_aceptacion, 
    hora_final, fecha_final, name, lastname, teacher, casetero, topic, grupo, number_group, laboratory, 
    tipo_vale, reporte, i_material) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
    data = (
        identificacion, solicitud[0], horario[1], horario[0], horario[1], horario[0],
        horario[1], horario[0], solicitud[1], solicitud[2], solicitud[6],
        casetero, solicitud[3], solicitud[4], solicitud[7],
        solicitud[8], solicitud[5], solicitud[9], materiales,
    )
    agregarDatosDB_Individual(sql, data)