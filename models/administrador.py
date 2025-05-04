from config.database import *

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