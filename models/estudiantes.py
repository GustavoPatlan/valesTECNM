from config.database import *

def horarios():
    """
    Obtiene todos los registros de horarios disponibles en la base de datos.
    """
    sql = "SELECT * FROM horarios"
    resultado = obtenerDatosDB_Varios(sql)
    return resultado

def obtenerEstudianteDB(ncontrol):
    """
    Obtiene los datos de un estudiante específico de la base de datos usando su número de control.
    
    Parámetros:
        ncontrol: Número de control del estudiante a buscar.
    
    Resultado:
        resultado: Datos del estudiante si existe, None si no se encuentra.
    """
    sql = "SELECT * FROM usuarios WHERE ncontrol = %s"
    data = (ncontrol,)
    resultado = obtenerDatosDB(sql, data)
    return resultado

def actualizarDatosEstudianteDB(nombres, apellidos, ncontrol):
    """
    Actualiza los datos personales de un estudiante en la base de datos.

    Parámetros:
        nombres: Nuevo nombre(s) del estudiante.
        apellidos: Nuevo apellido(s) del estudiante.
        ncontrol: Número de control que identifica al estudiante.
    """
    sql = "UPDATE usuarios SET nombres = %s, apellidos = %s WHERE ncontrol = %s"
    data = (nombres, apellidos, ncontrol,)
    agregarDatosDB_Individual(sql, data)

def actualizarLlaveEstudianteDB(llave, ncontrol):
    """
    Actualiza la contraseña de un estudiante en la base de datos.

    Parámetros:
        llave: Nueva contraseña.
        ncontrol: Número de control del estudiante.
    """
    sql = "UPDATE usuarios SET llave = %s WHERE ncontrol = %s"
    data = (llave, ncontrol,)
    agregarDatosDB_Individual(sql, data)

def maestros_registrados():
    """
    Obtiene la lista completa de maestros registrados en la base de datos,
    ordenados alfabéticamente por su nombre.
    """
    sql = "SELECT nombres, apellidos FROM maestros ORDER BY nombres"
    resultado = obtenerDatosDB_Varios(sql)
    return resultado

def material_registrado_estudiante():
    """
    Obtiene el listado completo de equipos disponibles en todos los laboratorios,
    con su respectiva clasificación por tipo de laboratorio.

    Realiza tres consultas distintas para obtener los equipos únicos de cada laboratorio
    y los combina en una sola lista con su identificación de laboratorio correspondiente.
    """
    sqls = [
        "SELECT DISTINCT EQUIPO FROM labpotencia",
        "SELECT DISTINCT EQUIPO FROM labelectronica",
        "SELECT DISTINCT EQUIPO FROM labthird"
    ]
    resultados = obtenerDatosDB_VariosSQL(sqls)
    resultado_1 = [(equipo[0], "POT") for equipo in resultados[0]]
    resultado_2 = [(equipo[0], "A/D") for equipo in resultados[1]]
    resultado_3 = [(equipo[0], "S/D") for equipo in resultados[2]]
    return resultado_1 + resultado_2 + resultado_3

def obtener_numeracion_laboratorio(laboratorio):
    """
    Obtiene el listado de equipos disponibles con su numeración correspondiente
    para un laboratorio específico.
    """
    if laboratorio == 'Y1' or laboratorio == 'Y2':
        salon = 'labpotencia'
    elif laboratorio == 'Y6' or laboratorio == 'Y7':
        salon = 'labelectronica'
    elif laboratorio == 'Y8':
        salon = 'labthird'
    sql = f"SELECT DISTINCT EQUIPO, NUMERACION FROM {salon}"
    resultado = obtenerDatosDB_Varios(sql)
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

def vale_existente_estudiante(identificacion):
    """
    Verifica si existe una solicitud de vale asociada a un identificador específico en la base de datos.

    Este método busca coincidencias parciales del identificador en el campo id_ncontrol
    de la tabla solicitud, útil para encontrar vales relacionados con un mismo estudiante
    o grupo de operaciones.

    Resultado:
        resultado: Tupla con las listas, None si no se encuentra.
    """
    sql = "SELECT * FROM solicitud WHERE id_ncontrol LIKE %s"
    data = (f"%{identificacion}%",)
    resultado = obtenerDatosDB(sql, data)
    return resultado

def registrarSolicitudEstudiante(identificacion, ncontrol, hora, fecha, nombre, apellido, 
                                 profesor, materia, grupo, alumnos, laboratorio, estado, vale, material):
    """
    Registra una nueva solicitud de vale de laboratorio en la base de datos.

    Parámetros:
        identificacion: ID único generado para la solicitud.
        ncontrol: Número de control del estudiante solicitante.
        hora: Hora de solicitud.
        fecha: Fecha de solicitud.
        nombre: Nombre(s) del estudiante.
        apellido: Apellido(s) del estudiante.
        profesor: Nombre del profesor responsable.
        materia: Nombre de la materia asociada.
        grupo: Grupo del estudiante.
        alumnos: Número de alumnos involucrados.
        laboratorio: Laboratorio solicitado.
        estado: Estado inicial de la solicitud.
        vale: Tipo de vale.
        material: Materiales solicitados.
    """
    sql = '''INSERT INTO solicitud 
                (id_ncontrol, ncontrol, hora_solicitud, fecha_solicitud, hora_aceptacion, fecha_aceptacion,
                name, lastname, teacher, topic, grupo, number_group, laboratory, estado, tipo_vale, reporte, material) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s ,%s, %s, %s)'''
    data = (identificacion, ncontrol, hora, fecha, 'N/A', 'N/A', nombre, apellido, profesor, materia, grupo, alumnos,
            laboratorio, estado, vale, 'N/A', material,)
    agregarDatosDB_Individual(sql, data)

def revisionVale(identificacion, hora, fecha, profesor, materia, grupo, alumnos, 
                 laboratorio, estado, vale, material):
    sql = '''UPDATE solicitud SET hora_solicitud = %s, fecha_solicitud = %s, teacher = %s, topic = %s, grupo = %s, 
             number_group = %s, laboratory = %s, estado = %s, tipo_vale = %s, material = %s WHERE id_ncontrol = %s'''
    data = (hora, fecha, profesor, materia, grupo, alumnos, laboratorio, estado, vale, material, identificacion,)
    agregarDatosDB_Individual(sql, data)

def valesSolicitadosEstudiantes(ncontrol):
    """
    Obtiene todos los vales solicitados por un estudiante específico, ordenados cronológicamente.

    Parámetros:
        ncontrol: Número de control del estudiante.
    """
    sql = "SELECT * FROM solicitud WHERE ncontrol LIKE %s ORDER BY fecha_solicitud ASC"
    data = (f"%{ncontrol}%",)
    resultado = obtenerDatosDB_Varios(sql, data)
    return resultado

def eliminarSolicitudEstudiante(identificacion):
    """
    Elimina una solicitud de vale específica de la base de datos usando su ID único.

    Parámetros:
        identificacion: ID único de la solicitud a eliminar.
    """
    sql = "DELETE FROM solicitud WHERE id_ncontrol = %s"
    data = (identificacion,)
    agregarDatosDB_Individual(sql, data)