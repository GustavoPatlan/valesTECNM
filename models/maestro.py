from config.database import *

lab_material = {
        'Y1': "labpotencia",
        'Y2': "labpotencia",
        'Y6': "labelectronica",
        'Y7': "labelectronica",
        'Y8': "labthird"
    }

def valesParaMaestro(name):
    """
    Obtiene estadísticas de vales asociados a un maestro, clasificados por estado.

    Parámetros:
        name: Nombre completo del maestro.

    Consulta SQL:
        Realiza un conteo de vales agrupados en tres categorías:
        1. Vales ACTIVOS.
        2. Vales EN ESPERA.
        3. Vales SIN ACEPTAR.
        Solo considera vales de tipo LABORATORIO o PROYECTO.

    Resultado:
        Diccionario con tres claves:
            - "activo": Cantidad de vales activos.
            - "espera": Cantidad de vales en espera.
            - "sin": Cantidad de vales sin aceptar.
    """
    sql = """SELECT COUNT(*) AS total,
                SUM(CASE WHEN estado = 'ACTIVO' THEN 1 ELSE 0 END) AS total_activo,
                SUM(CASE WHEN estado = 'EN ESPERA' THEN 1 ELSE 0 END) AS total_en_espera,
                SUM(CASE WHEN estado = 'SIN ACEPTAR' THEN 1 ELSE 0 END) AS total_sin_aceptar
            FROM solicitud
            WHERE teacher = %s AND (tipo_vale = 'LABORATORIO' OR tipo_vale = 'PROYECTO')"""
    data = (name,)
    resultado = obtenerDatosDB(sql, data)

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

def valesParaMaestroFirma(name):
    """
    Obtiene todas las solicitudes de vales pendientes de aceptación para un maestro específico.

    Parámetros:
        name: Nombre completo del maestro.

    Retorno:
        Lista de tuplas con todos los campos de las solicitudes pendientes, donde cada tupla contiene:
              - Todos los campos de la tabla 'solicitud' en el orden original.
              - Ordenadas cronológicamente.
              - Lista vacía si no hay solicitudes pendientes.
    """
    sql = """SELECT * FROM solicitud
             WHERE teacher = %s AND estado = 'SIN ACEPTAR'
             ORDER BY fecha_solicitud ASC"""
    data = (name,)
    resultado = obtenerDatosDB_Varios(sql, data)
    return resultado

def valesParaMaestroAceptados(name):
    """
    Obtiene las solicitudes de vales aceptadas o en espera de los estudiantes para un maestro.

    Parámetros:
        name: Nombre completo del maestro.

    Retorno:
        Lista de tuplas con los vales que cumplen:
            - Asignados al maestro.
            - En estado 'EN ESPERA' o 'ACTIVO'.
            - De tipo LABORATORIO o PROYECTO.
            - Ordenados por fecha más antigua primero.
    """
    sql = """SELECT * FROM solicitud
             WHERE teacher = %s AND (estado = 'EN ESPERA' OR estado = 'ACTIVO')
             AND (tipo_vale = 'LABORATORIO' OR tipo_vale = 'PROYECTO')
             ORDER BY fecha_solicitud ASC"""
    data = (name,)
    resultado = obtenerDatosDB_Varios(sql, data)
    return resultado
    
def registroMaestros(name):
    """
    Obtiene el registro de vales asociados a un maestro específico.

    Parámetros:
        name: Nombre completo del maestro.

    Consulta:
        - Recupera TODOS los campos de los vales registrados.
        - Ordena por fecha_final.

    Retorno:
        Lista de tuplas con todos los campos de los vales encontrados:
              - Ordenados por fecha_final.
              - Filtra por tipo de vale.
              - Lista vacía si no hay coincidencias.
    """
    sql = """SELECT * FROM registro
             WHERE teacher = %s AND (tipo_vale = 'LABORATORIO' OR tipo_vale = 'PROYECTO')
             ORDER BY fecha_final ASC"""
    data = (name,)
    resultado = obtenerDatosDB_Varios(sql, data)
    return resultado

def registroMaestrosPersonal(name):
    """
    Obtiene el registro completo de vales de un maestro ordenados por fecha.

    Parámetros:
        name : ID del maestro.
    """
    sql = "SELECT * FROM registro WHERE ncontrol = %s ORDER BY fecha_final ASC"
    data = (name,)
    resultado = obtenerDatosDB_Varios(sql, data)
    return resultado

def valesActivosMaestros(name):
    """
    Obtiene todos los vales asociados a un maestro, ordenados cronológicamente.

    Parámetros:
        name: ID del maestro.
    """
    sql = "SELECT * FROM solicitud WHERE ncontrol = %s ORDER BY fecha_solicitud ASC"
    data = (name,)
    resultado = obtenerDatosDB_Varios(sql, data)
    return resultado

def valesParaMaestroAceptar(identificacion):
    """
    Cambia el estado de una solicitud a 'EN ESPERA' para aceptación posterior.

    Parámetros:
        identificacion: ID completo del vale a actualizar.
    """
    sql = "UPDATE solicitud SET estado = 'EN ESPERA' WHERE id_ncontrol = %s"
    data = (identificacion,)
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
    Cambia el estado de una solicitud a 'REVISION' para observacion del alumno.

    Parámetros:
        identificacion: ID completo del vale a actualizar.
    """
    sql = "UPDATE solicitud SET estado = 'REVISION' WHERE id_ncontrol = %s"
    data = (identificacion,)
    agregarDatosDB_Individual(sql, data)

def materialMaestro():
    """
    Obtiene el listado completo de equipos disponibles en todos los laboratorios.

    Proceso:
        1. Realiza 3 consultas SQL paralelas para obtener equipos disponibles de:
        - Laboratorio de Potencia (POT).
        - Laboratorio de Electrónica (A/D).
        - Laboratorio Third (S/D).
        2. Combina y formatea los resultados con identificador de laboratorio

    Retorno:
        Lista unificada de tuplas.
    """
    sqls = [
        "SELECT EQUIPO, N_CASETA, NUMERACION FROM labpotencia WHERE disponibilidad = 'DISPONIBLE'",
        "SELECT EQUIPO, N_CASETA, NUMERACION FROM labelectronica WHERE disponibilidad = 'DISPONIBLE'",
        "SELECT EQUIPO, N_CASETA, NUMERACION FROM labthird WHERE disponibilidad = 'DISPONIBLE'"
    ]
    resultados = obtenerDatosDB_VariosSQL(sqls)
    resultado_1 = [(equipo[0], equipo[1], equipo[2], "POT") for equipo in resultados[0]]
    resultado_2 = [(equipo[0], equipo[1], equipo[2], "A/D") for equipo in resultados[1]]
    resultado_3 = [(equipo[0], equipo[1], equipo[2], "S/D") for equipo in resultados[2]]
    return resultado_1 + resultado_2 + resultado_3

def registrarSolicitudMaestro(identificacion, ncontrol, hora, fecha, nombre, apellido, 
                                 profesor, materia, grupo, alumnos, laboratorio, estado, vale, material):
    """
    Registra una nueva solicitud de vale realizada por un maestro en la base de datos.

    Parámetros:
        identificacion: ID único generado para la solicitud.
        ncontrol: ID del maestro.
        hora: Hora de solicitud.
        fecha: Fecha de solicitud.
        nombre: Nombre(s) del maestro beneficiario.
        apellido: Apellido(s) del maestro beneficiario.
        profesor: Nombre del maestro solicitante.
        materia: Materia asociada a la solicitud.
        grupo: Grupo.
        alumnos: Número de alumnos beneficiarios.
        laboratorio: Laboratorio solicitado.
        estado: Estado inicial de la solicitud.
        vale: Tipo de vale.
        material: Materiales solicitados.
    """
    sql = '''INSERT INTO solicitud 
                (id_ncontrol, ncontrol, hora_solicitud, fecha_solicitud, hora_aceptacion, fecha_aceptacion,
                name, lastname, teacher, topic, grupo, number_group, laboratory, estado, tipo_vale, reporte, material) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s ,%s, %s, %s)'''
    data = (identificacion, ncontrol, hora, fecha, hora, fecha, nombre, apellido, profesor, materia, grupo, alumnos,
            laboratorio, 'ACTIVO', 'MAESTRO', 'N/A', material,)
    agregarDatosDB_Individual(sql, data)

def materialAsignado(laboratorio, materiales):
    """
    Actualiza el estado de un material a 'OCUPADO' cuando es asignado a un laboratorio.

    Parámetros:
        laboratorio: Nombre del laboratorio.
        materiales: Datos del material en formato.
    """
    condition = lab_material.get(laboratorio)
    sql = f"UPDATE {condition} SET DISPONIBILIDAD = 'OCUPADO' WHERE EQUIPO = %s AND N_CASETA = %s AND NUMERACION = 'SI'"
    data = (materiales,)
    agregarDatosDB_Individual_for(sql, data)

def actualizarLlaveMaestroDB(llave, ncontrol):
    """
    Actualiza la contraseña de un maestro en la base de datos.

    Parámetros:
        llave: Nueva contraseña.
        id: Identificación del maestro.
    """
    sql = "UPDATE maestros SET llave = %s WHERE id = %s"
    data = (llave, ncontrol,)
    agregarDatosDB_Individual(sql, data)