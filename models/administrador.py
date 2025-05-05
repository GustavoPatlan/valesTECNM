from config.database import *

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
    if data[3] == '':
        sql = "UPDATE administrador SET nombres = %s, apellidos = %s WHERE id = %s"
        query = (data[1], data[2], data[0],)
    else:
        sql = "UPDATE administrador SET nombres = %s, apellidos = %s, llave = %s WHERE id = %s"
        query = (data[1], data[2], data[3], data[0],)
    agregarDatosDB_Individual(sql, query)

def agregarHorario(data):
    sql = 'INSERT INTO horarios (dia, laboratorio, hora_i, hora_f) VALUES (%s, %s, %s, %s)'
    query = (data[0], data[1], data[2], data[3],)
    agregarDatosDB_Individual(sql, query)

def eliminarHorario(data):
    sql = f"DELETE FROM horarios WHERE dia = '{data[0]}' AND laboratorio = '{data[1]}' AND hora_i = '{data[2]}' AND hora_f = '{data[3]}'"
    agregarDatosDB_Individual(sql)

def estudiantesRegistrados():
    sql = "SELECT ncontrol, laboratorio, proyecto, correo, carrera, nombres, apellidos FROM usuarios"
    resultado = obtenerDatosDB_Varios(sql)
    return resultado

def actualizarDatosUsuario(data):
    if data[0] == data[1]:
        sql = "UPDATE usuarios SET carrera = %s, nombres = %s, apellidos = %s WHERE ncontrol = %s"
        query = (data[3], data[4], data[5], data[0],)
    else:
        sql = "UPDATE usuarios SET ncontrol = %s, correo = %s, carrera = %s, nombres = %s, apellidos = %s WHERE ncontrol = %s"
        query = (data[1], data[2], data[3], data[4], data[5], data[0],)
    agregarDatosDB_Individual(sql, query)

def estudianteExistente(ncontrol):
    sql = "SELECT ncontrol FROM usuarios WHERE ncontrol = %s"
    query =(ncontrol,)
    resultado = obtenerDatosDB(sql, query)
    return resultado

def estudianteEliminado(ncontrol):
    sql = f"DELETE FROM usuarios WHERE ncontrol = '{ncontrol}'"
    agregarDatosDB_Individual(sql)

def administradorLlave(identificacion):
    sql = f"SELECT llave FROM administrador WHERE id = '{identificacion}'"
    resultado = obtenerDatosDB(sql)
    return resultado

def resetearEstudiantes():
    sql = "DELETE FROM usuarios"
    agregarDatosDB_Individual(sql)

def maestrosRegistrados():
    sql = "SELECT * FROM maestros"
    resultado = obtenerDatosDB_Varios(sql)
    return resultado

def actualizarDatosMaestro(data):
    if data[0] == data[1]:
        sql = "UPDATE maestros SET correo = %s, nombres = %s, apellidos = %s, llave = %s WHERE id = %s"
        query = (data[2], data[3], data[4], data[5], data[0],)
    else:
        sql = "UPDATE maestros SET id = %s, correo = %s, nombres = %s, apellidos = %s, llave = %s WHERE id = %s"
        query = (data[1], data[2], data[3], data[4], data[5], data[0],)
    agregarDatosDB_Individual(sql, query)

def maestroExistente(ncontrol):
    sql = "SELECT id FROM maestros WHERE id = %s"
    query =(ncontrol,)
    resultado = obtenerDatosDB(sql, query)
    return resultado

def maestroEliminado(ncontrol):
    sql = f"DELETE FROM maestros WHERE id = '{ncontrol}'"
    agregarDatosDB_Individual(sql)

def agregarMaestroDB(data):
    sql = 'INSERT INTO maestros (id, correo, nombres, apellidos, llave) VALUES (%s, %s, %s, %s, %s)'
    query = (data[0], data[1], data[2], data[3], data[4],)
    agregarDatosDB_Individual(sql, query)

def caseterosRegistrados():
    sql = "SELECT * FROM caseteros"
    resultado = obtenerDatosDB_Varios(sql)
    return resultado

def actualizarDatosCasetero(data):
    if data[0] == data[1]:
        sql = "UPDATE caseteros SET correo = %s, nombres = %s, apellidos = %s, llave = %s, laboratorio = %s WHERE id = %s"
        query = (data[3], data[4], data[5], data[6], data[2], data[0],)
    else:
        sql = "UPDATE caseteros SET id = %s, correo = %s, nombres = %s, apellidos = %s, llave = %s, laboratorio = %s WHERE id = %s"
        query = (data[1], data[3], data[4], data[5], data[6], data[2], data[0],)
    agregarDatosDB_Individual(sql, query)

def caseteroExistente(ncontrol):
    sql = "SELECT id FROM caseteros WHERE id = %s"
    query =(ncontrol,)
    resultado = obtenerDatosDB(sql, query)
    return resultado

def caseteroEliminado(ncontrol):
    sql = f"DELETE FROM caseteros WHERE id = '{ncontrol}'"
    agregarDatosDB_Individual(sql)

def agregarCaseteroDB(data):
    sql = 'INSERT INTO caseteros (id, correo, nombres, apellidos, llave, laboratorio) VALUES (%s, %s, %s, %s, %s, %s)'
    query = (data[0], data[2], data[3], data[4], data[5], data[1],)
    agregarDatosDB_Individual(sql, query)

def valesActivos():
    sql = "SELECT * FROM solicitud WHERE estado = 'ACTIVO' ORDER BY fecha_solicitud ASC"
    resultado = obtenerDatosDB_Varios(sql)
    return resultado

def valesEnEspera():
    sql = "SELECT * FROM solicitud WHERE estado = 'EN ESPERA' ORDER BY fecha_solicitud ASC"
    resultado = obtenerDatosDB_Varios(sql)
    return resultado

def valesSinAceptar():
    sql = "SELECT * FROM solicitud WHERE estado = 'SIN ACEPTAR' ORDER BY fecha_solicitud ASC"
    resultado = obtenerDatosDB_Varios(sql)
    return resultado

def materialLaboratorio(laboratorio):
    condition = lab_material.get(laboratorio)
    # Consulta 1: Obtiene todos los materiales con ordenamiento específico.
    sql = f"SELECT * FROM ({condition}) ORDER BY NUMERACION DESC, EQUIPO, N_CASETA ASC"
    resultado = obtenerDatosDB_Varios(sql)
    return resultado

def registros():
    sql = f"SELECT * FROM registro ORDER BY fecha_final ASC"
    resultado = obtenerDatosDB_Varios(sql)
    return resultado

def resetearRegistros():
    sql = "DELETE FROM registro"
    agregarDatosDB_Individual(sql)

def solicitudActiva(ncontrol):
    sql = f"SELECT ncontrol FROM solicitud WHERE ncontrol = '{ncontrol}'"
    resultado = obtenerDatosDB(sql)
    return resultado