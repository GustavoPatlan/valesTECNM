from config.database import *

# Mapeo de laboratorios a sus respectivas tablas en la base de datos.
lab_material = {
        'Y1-Y2': "labpotencia",
        'Y6-Y7': "labelectronica",
        'Y8': "labthird"
    }

def horarios():
    """
    Obtiene todos los registros de horarios disponibles en la base de datos.
    """
    sql = "SELECT * FROM horarios"
    resultado = obtenerDatosDB_Varios(sql)
    return resultado

def actualizarDatos(data):
    """
    Actualiza la información de un administrador en la base de datos.
    Puede actualizar o no la llave de acceso.
    """
    if data[3] == '':
        sql = "UPDATE administrador SET nombres = %s, apellidos = %s WHERE id = %s"
        query = (data[1], data[2], data[0],)
    else:
        sql = "UPDATE administrador SET nombres = %s, apellidos = %s, llave = %s WHERE id = %s"
        query = (data[1], data[2], data[3], data[0],)
    agregarDatosDB_Individual(sql, query)

def agregarHorario(data):
    """
    Agrega un nuevo horario a la base de datos con día, laboratorio y horario especificado.
    """
    sql = 'INSERT INTO horarios (dia, laboratorio, hora_i, hora_f) VALUES (%s, %s, %s, %s)'
    query = (data[0], data[1], data[2], data[3],)
    agregarDatosDB_Individual(sql, query)

def eliminarHorario(data):
    """
    Elimina un horario específico de la base de datos.
    """
    sql = f"DELETE FROM horarios WHERE dia = '{data[0]}' AND laboratorio = '{data[1]}' AND hora_i = '{data[2]}' AND hora_f = '{data[3]}'"
    agregarDatosDB_Individual(sql)

def estudiantesRegistrados():
    """
    Obtiene la lista completa de estudiantes registrados en el sistema con todos sus datos, excepto la contraseña.
    """
    sql = "SELECT ncontrol, laboratorio, proyecto, correo, carrera, nombres, apellidos FROM usuarios"
    resultado = obtenerDatosDB_Varios(sql)
    return resultado

def actualizarDatosUsuario(data):
    """
    Actualiza los datos de un estudiante en la base de datos.
    """
    if data[0] == data[1]:
        sql = "UPDATE usuarios SET carrera = %s, nombres = %s, apellidos = %s WHERE ncontrol = %s"
        query = (data[3], data[4], data[5], data[0],)
    else:
        sql = "UPDATE usuarios SET ncontrol = %s, correo = %s, carrera = %s, nombres = %s, apellidos = %s WHERE ncontrol = %s"
        query = (data[1], data[2], data[3], data[4], data[5], data[0],)
    agregarDatosDB_Individual(sql, query)

def estudianteExistente(ncontrol):
    """
    Verifica si un estudiante existe en la base de datos mediante su número de control.
    """
    sql = "SELECT ncontrol FROM usuarios WHERE ncontrol = %s"
    query =(ncontrol,)
    resultado = obtenerDatosDB(sql, query)
    return resultado

def estudianteEliminado(ncontrol):
    """
    Elimina un estudiante de la base de datos usando su número de control.
    """
    sql = f"DELETE FROM usuarios WHERE ncontrol = '{ncontrol}'"
    agregarDatosDB_Individual(sql)

def administradorLlave(identificacion):
    """
    Obtiene la llave de acceso de un administrador específico.
    """
    sql = f"SELECT llave FROM administrador WHERE id = '{identificacion}'"
    resultado = obtenerDatosDB(sql)
    return resultado

def resetearEstudiantes():
    """
    Elimina todos los estudiantes de la base de datos.
    """
    sql = "DELETE FROM usuarios"
    agregarDatosDB_Individual(sql)

def maestrosRegistrados():
    """
    Obtiene la lista completa de maestros registrados en el sistema.
    """
    sql = "SELECT * FROM maestros"
    resultado = obtenerDatosDB_Varios(sql)
    return resultado

def actualizarDatosMaestro(data):
    """
    Actualiza los datos de un maestro en la base de datos.
    """
    if data[0] == data[1]:
        sql = "UPDATE maestros SET correo = %s, nombres = %s, apellidos = %s, llave = %s WHERE id = %s"
        query = (data[2], data[3], data[4], data[5], data[0],)
    else:
        sql = "UPDATE maestros SET id = %s, correo = %s, nombres = %s, apellidos = %s, llave = %s WHERE id = %s"
        query = (data[1], data[2], data[3], data[4], data[5], data[0],)
    agregarDatosDB_Individual(sql, query)

def maestroExistente(ncontrol):
    """
    Verifica si un maestro existe en la base de datos mediante su ID.
    """
    sql = "SELECT id FROM maestros WHERE id = %s"
    query =(ncontrol,)
    resultado = obtenerDatosDB(sql, query)
    return resultado

def maestroEliminado(ncontrol):
    """
    Elimina un maestro de la base de datos usando su ID.
    """
    sql = f"DELETE FROM maestros WHERE id = '{ncontrol}'"
    agregarDatosDB_Individual(sql)

def agregarMaestroDB(data):
    """
    Agrega un nuevo maestro a la base de datos con todos sus datos.
    """
    sql = 'INSERT INTO maestros (id, correo, nombres, apellidos, llave) VALUES (%s, %s, %s, %s, %s)'
    query = (data[0], data[1], data[2], data[3], data[4],)
    agregarDatosDB_Individual(sql, query)

def caseterosRegistrados():
    """
    Obtiene la lista completa de caseteros registrados en el sistema.
    """
    sql = "SELECT * FROM caseteros"
    resultado = obtenerDatosDB_Varios(sql)
    return resultado

def actualizarDatosCasetero(data):
    """
    Actualiza los datos de un casetero en la base de datos.
    """
    if data[0] == data[1]:
        sql = "UPDATE caseteros SET correo = %s, nombres = %s, apellidos = %s, llave = %s, laboratorio = %s WHERE id = %s"
        query = (data[3], data[4], data[5], data[6], data[2], data[0],)
    else:
        sql = "UPDATE caseteros SET id = %s, correo = %s, nombres = %s, apellidos = %s, llave = %s, laboratorio = %s WHERE id = %s"
        query = (data[1], data[3], data[4], data[5], data[6], data[2], data[0],)
    agregarDatosDB_Individual(sql, query)

def caseteroExistente(ncontrol):
    """
    Verifica si un casetero existe en la base de datos mediante su ID.
    """
    sql = "SELECT id FROM caseteros WHERE id = %s"
    query =(ncontrol,)
    resultado = obtenerDatosDB(sql, query)
    return resultado

def caseteroEliminado(ncontrol):
    """
    Elimina un casetero de la base de datos usando su ID.
    """
    sql = f"DELETE FROM caseteros WHERE id = '{ncontrol}'"
    agregarDatosDB_Individual(sql)

def agregarCaseteroDB(data):
    """
    Agrega un nuevo casetero a la base de datos con todos sus datos.
    """
    sql = 'INSERT INTO caseteros (id, correo, nombres, apellidos, llave, laboratorio) VALUES (%s, %s, %s, %s, %s, %s)'
    query = (data[0], data[2], data[3], data[4], data[5], data[1],)
    agregarDatosDB_Individual(sql, query)

def valesActivos():
    """
    Obtiene todos los vales que están actualmente activos en el sistema.
    """
    sql = "SELECT * FROM solicitud WHERE estado = 'ACTIVO' ORDER BY fecha_solicitud ASC"
    resultado = obtenerDatosDB_Varios(sql)
    return resultado

def valesEnEspera():
    """
    Obtiene todos los vales que están en estado de espera.
    """
    sql = "SELECT * FROM solicitud WHERE estado = 'EN ESPERA' ORDER BY fecha_solicitud ASC"
    resultado = obtenerDatosDB_Varios(sql)
    return resultado

def valesSinAceptar():
    """
    Obtiene todos los vales que no han sido aceptados aún.
    """
    sql = "SELECT * FROM solicitud WHERE estado = 'SIN ACEPTAR' ORDER BY fecha_solicitud ASC"
    resultado = obtenerDatosDB_Varios(sql)
    return resultado

def materialLaboratorio(laboratorio):
    """
    Obtiene el inventario de materiales de un laboratorio específico.
    Los resultados están ordenados por numeración, equipo y número de caseta.
    """
    condition = lab_material.get(laboratorio)
    sql = f"SELECT * FROM ({condition}) ORDER BY NUMERACION DESC, EQUIPO, N_CASETA ASC"
    resultado = obtenerDatosDB_Varios(sql)
    return resultado

def registros():
    """
    Obtiene todos los registros del sistema, ordenados por fecha final.
    """
    sql = f"SELECT * FROM registro ORDER BY fecha_final ASC"
    resultado = obtenerDatosDB_Varios(sql)
    return resultado

def resetearRegistros():
    """
    Elimina todos los registros almacenados en la base de datos.
    """
    sql = "DELETE FROM registro"
    agregarDatosDB_Individual(sql)

def solicitudActiva(ncontrol):
    """
    Verifica si un usuario tiene una solicitud activa mediante su número de control.
    """
    sql = f"SELECT ncontrol FROM solicitud WHERE ncontrol = '{ncontrol}'"
    resultado = obtenerDatosDB(sql)
    return resultado