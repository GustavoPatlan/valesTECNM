from config.database import *

lab_material = {
        'Y1': "labpotencia",
        'Y2': "labpotencia",
        'Y6': "labelectronica",
        'Y7': "labelectronica",
        'Y8': "labthird"
    }

def valesParaMaestro(name):
    sql = """SELECT COUNT(*) AS total,
                SUM(CASE WHEN estado = 'ACTIVO' THEN 1 ELSE 0 END) AS total_activo,
                SUM(CASE WHEN estado = 'EN ESPERA' THEN 1 ELSE 0 END) AS total_en_espera,
                SUM(CASE WHEN estado = 'SIN ACEPTAR' THEN 1 ELSE 0 END) AS total_sin_aceptar
            FROM solicitud
            WHERE teacher = %s AND (tipo_vale = 'LABORATORIO' OR tipo_vale = 'PROYECTO')"""
    
    data = (name,)
    resultado = obtenerDatosDB(sql, data)
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
    sql = """SELECT * FROM solicitud
             WHERE teacher = %s AND estado = 'SIN ACEPTAR'
             ORDER BY fecha_solicitud ASC"""
    
    data = (name,)
    resultado = obtenerDatosDB_Varios(sql, data)
    return resultado

def valesParaMaestroAceptados(name):
    sql = """SELECT * FROM solicitud
             WHERE teacher = %s AND (estado = 'EN ESPERA' OR estado = 'ACTIVO')
             AND (tipo_vale = 'LABORATORIO' OR tipo_vale = 'PROYECTO')
             ORDER BY fecha_solicitud ASC"""
    data = (name,)
    resultado = obtenerDatosDB_Varios(sql, data)
    return resultado
    
def registroMaestros(name):
    sql = """SELECT * FROM registro
             WHERE teacher = %s AND (tipo_vale = 'LABORATORIO' OR tipo_vale = 'PROYECTO')
             ORDER BY fecha_final ASC"""
    data = (name,)
    resultado = obtenerDatosDB_Varios(sql, data)
    return resultado

def registroMaestrosPersonal(name):
    sql = "SELECT * FROM registro WHERE ncontrol = %s ORDER BY fecha_final ASC"
    data = (name,)
    resultado = obtenerDatosDB_Varios(sql, data)
    return resultado

def valesActivosMaestros(name):
    sql = "SELECT * FROM solicitud WHERE ncontrol = %s ORDER BY fecha_solicitud ASC"
    data = (name,)
    resultado = obtenerDatosDB_Varios(sql, data)
    return resultado

def valesParaMaestroAceptar(identificacion): # Método para poner una solicitud en espera.
    sql = "UPDATE solicitud SET estado = 'EN ESPERA' WHERE id_ncontrol = %s"
    data = (identificacion,)
    agregarDatosDB_Individual(sql, data)

def vale_existente_estudiante(identificacion): # Método para seleccionar una solcitud de vale de un usuario en específico.
    sql = "SELECT * FROM solicitud WHERE id_ncontrol LIKE %s"
    data = (f"%{identificacion}%",)
    resultado = obtenerDatosDB(sql, data)
    return resultado

def obtenerEstudianteDB(ncontrol):
    sql = "SELECT proyecto FROM usuarios WHERE ncontrol = %s"
    data = (ncontrol,)
    resultado = obtenerDatosDB(sql, data)
    return resultado

def vales_cantidad(vale, cantidad, ncontrol):
    if vale == 'PROYECTO':
        sql = "UPDATE usuarios SET proyecto = %s WHERE ncontrol = %s"
    else:
        sql = "UPDATE usuarios SET laboratorio = %s WHERE ncontrol = %s"
    data = (cantidad, ncontrol,)
    agregarDatosDB_Individual(sql, data)

def eliminarSolicitudEstudiante(identificacion): # Método para elimnar una solicitud.
    sql = "DELETE FROM solicitud WHERE id_ncontrol = %s"
    data = (identificacion,)
    agregarDatosDB_Individual(sql, data)

def materialMaestro(): # Método para seleccionar el equipo y numeracion de todos los laboratorios.
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
    sql = '''INSERT INTO solicitud 
                (id_ncontrol, ncontrol, hora_solicitud, fecha_solicitud, hora_aceptacion, fecha_aceptacion,
                name, lastname, teacher, topic, grupo, number_group, laboratory, estado, tipo_vale, reporte, material) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s ,%s, %s, %s)'''
    data = (identificacion, ncontrol, hora, fecha, hora, fecha, nombre, apellido, profesor, materia, grupo, alumnos,
            laboratorio, estado, 'MAESTRO', 'N/A', material,)
    agregarDatosDB_Individual(sql, data)

def materialAsignado(laboratorio, materiales):
    condition = lab_material.get(laboratorio)
    sql = f"UPDATE {condition} SET DISPONIBILIDAD = 'OCUPADO' WHERE EQUIPO = %s AND N_CASETA = %s AND NUMERACION = 'SI'"
    data = (materiales,)
    agregarDatosDB_Individual_for(sql, data)