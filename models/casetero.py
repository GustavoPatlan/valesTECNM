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
    condition = lab_conditions.get(laboratorio)
    sql = f"SELECT * FROM solicitud WHERE estado = 'EN ESPERA' AND ({condition})"
    resultado = obtenerDatosDB_Varios(sql)
    return resultado

def valesParaCaseteroActivo(laboratorio):
    condition = lab_conditions.get(laboratorio)
    sql = f"SELECT * FROM solicitud WHERE estado = 'ACTIVO' AND ({condition}) AND (tipo_vale = 'LABORATORIO' OR tipo_vale = 'PROYECTO')"
    resultado = obtenerDatosDB_Varios(sql)
    return resultado

def valesParaCaseteroMaestro(laboratorio):
    condition = lab_conditions.get(laboratorio)
    sql = f"SELECT * FROM solicitud WHERE tipo_vale = 'MAESTRO' AND ({condition})"
    resultado = obtenerDatosDB_Varios(sql)
    return resultado

def obtenerMaterialCasetero(laboratorio):
    condition = lab_material.get(laboratorio)
    sql = f"SELECT EQUIPO, N_CASETA FROM {condition} WHERE NUMERACION = 'SI' AND disponibilidad = 'DISPONIBLE'"
    resultado = obtenerDatosDB_Varios(sql)
    return resultado

def materialAsignado(laboratorio, identificacion, materiales, horario):
    condition = lab_material.get(laboratorio)
    sql = f"UPDATE {condition} SET DISPONIBILIDAD = 'OCUPADO' WHERE EQUIPO = %s AND N_CASETA = %s AND NUMERACION = 'SI'"
    data = (materiales,)
    agregarDatosDB_Individual_for(sql, data)
    material = json.dumps(materiales)
    sql = "UPDATE solicitud SET material = %s, hora_aceptacion = %s, fecha_aceptacion = %s, estado = 'ACTIVO' WHERE id_ncontrol = %s"
    data = (material, horario[1], horario[0], identificacion,)
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

def reportarVale(identificacion, reporte='N/A'):
    sql = "UPDATE solicitud SET reporte = %s WHERE id_ncontrol = %s"
    data = (reporte, identificacion,)
    agregarDatosDB_Individual(sql, data)

def registrarVale(laboratorio, identificacion, materiales, horario, solicitud, casetero):
    condition = lab_material.get(laboratorio)
    sql = f"UPDATE {condition} SET DISPONIBILIDAD = 'DISPONIBLE' WHERE EQUIPO = %s AND N_CASETA = %s AND NUMERACION = 'SI'"
    data = (materiales,)
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
    sql = "DELETE FROM solicitud WHERE id_ncontrol = %s"
    data = (identificacion,)
    agregarDatosDB_Individual(sql, data)

def registroLaboratorio(laboratorio):
    condition = lab_conditions.get(laboratorio)
    sql = f"SELECT * FROM registro WHERE ({condition}) ORDER BY fecha_final ASC"
    resultado = obtenerDatosDB_Varios(sql)
    return resultado

def materialLaboratorio(laboratorio):
    condition = lab_material.get(laboratorio)
    sql = f"SELECT * FROM ({condition}) ORDER BY NUMERACION DESC, EQUIPO, N_CASETA ASC"
    resultado_1 = obtenerDatosDB_Varios(sql)
    sql = f"SELECT DISTINCT EQUIPO, NUMERACION FROM {condition}"
    resultado_2 = obtenerDatosDB_Varios(sql)
    return resultado_1, resultado_2

def materialLaboratorioChecar(laboratorio, equipo, caseta):
    condition = lab_material.get(laboratorio)
    sql = f"SELECT id FROM {condition} WHERE EQUIPO = %s AND N_CASETA = %s"
    data = (equipo, caseta,)
    resultado = obtenerDatosDB(sql, data)
    return resultado

def materialLaboratorioActualizar(laboratorio, identificacion, equipo, caseta, marca, modelo, serie, 
                           inventario, condicion, disponibilidad, voltaje = 'S/A', potencia = 'S/A', observaciones=''):
    condition = lab_material.get(laboratorio)
    sql = f"""UPDATE {condition} 
            SET EQUIPO = %s, N_CASETA = %s, MARCA = %s, MODELO = %s, N_SERIE = %s, N_INVENTARIO = %s, 
            VOLTAJE = %s, POTENCIA = %s, CONDICION = %s, DISPONIBILIDAD = %s, OBSERVACIONES = %s WHERE id = %s"""
    data = (equipo, caseta, marca, modelo, serie, inventario, voltaje, potencia, condicion, disponibilidad, observaciones, identificacion,)
    agregarDatosDB_Individual(sql, data)

def componenteLaboratorioModificar(laboratorio, identificacion, marca, modelo, cantidad, observaciones=''):
    condition = lab_material.get(laboratorio)
    sql = f"""
        UPDATE {condition}
        SET MARCA = %s, MODELO = %s, CANTIDAD = %s, OBSERVACIONES = %s
        WHERE id = %s
    """
    data = (marca, modelo, cantidad, observaciones, identificacion,)
    agregarDatosDB_Individual(sql, data)

def componenteLaboratorioBorrar(laboratorio, identificacion):
    condition = lab_material.get(laboratorio)
    sql = f"DELETE FROM {condition} WHERE id = %s"
    data = (identificacion,)
    agregarDatosDB_Individual(sql, data)

def agregarNuevoMaterial(laboratorio, equipo, marca, modelo, numeracion, caseta, serie, inventario, voltaje, potencia, cantidad = 1):
    condition = lab_material.get(laboratorio)
    sql = f'''INSERT INTO {condition}
    (EQUIPO, MARCA, MODELO, N_CASETA, N_SERIE, N_INVENTARIO, 
    VOLTAJE, POTENCIA, CANTIDAD, CONDICION, DISPONIBILIDAD, NUMERACION, OBSERVACIONES) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
    data = (equipo, marca, modelo, caseta, serie, inventario, voltaje, potencia, cantidad, 'OK', 'DISPONIBLE', numeracion, 'OK')
    agregarDatosDB_Individual(sql, data)

def materialLaboratorioVerificarCantidad(laboratorio, equipo, marca, modelo):
    condition = lab_material.get(laboratorio)
    sql = f"SELECT CANTIDAD FROM {condition} WHERE EQUIPO = %s AND MARCA = %s AND MODELO = %s AND NUMERACION = 'NO'"
    data = (equipo, marca, modelo,)
    resultado = obtenerDatosDB(sql, data)
    return resultado

def materialLaboratorioActualizarCantidad(laboratorio, cantidad, equipo, marca, modelo):
    condition = lab_material.get(laboratorio)
    sql = f"""UPDATE {condition} SET CANTIDAD = %s WHERE EQUIPO = %s AND MARCA = %s AND MODELO = %s AND NUMERACION = 'NO'"""
    data = (cantidad, equipo, marca, modelo,)
    agregarDatosDB_Individual(sql, data)

def obtenerMaterialCaseteroEditar(laboratorio):
    condition = lab_material.get(laboratorio)
    sql = f"SELECT EQUIPO, N_CASETA, NUMERACION FROM {condition} WHERE disponibilidad = 'DISPONIBLE'"
    resultado = obtenerDatosDB_Varios(sql)
    return resultado

def obtenerMaterialCaseteroRegistrar(laboratorio):
    condition = lab_material.get(laboratorio)
    sql = f"SELECT EQUIPO, N_CASETA, NUMERACION FROM {condition}"
    resultado = obtenerDatosDB_Varios(sql)
    return resultado

def materialReportado(laboratorio, materiales):
    condition = lab_material.get(laboratorio)
    sql = f"UPDATE {condition} SET OBSERVACIONES = %s, DISPONIBILIDAD = %s WHERE EQUIPO = %s AND N_CASETA = %s"
    data = (materiales,)
    agregarDatosDB_Individual_reporte(sql, data)

def editadoVale(identificacion, materiales):
    materiales = json.dumps(materiales)
    sql = "UPDATE solicitud SET material = %s WHERE id_ncontrol = %s"
    data = (materiales, identificacion,)
    agregarDatosDB_Individual(sql, data)

def maestros_registrados(): # Método para seleccionar todos los maestros ordenados por nombre.
    sql = "SELECT nombres, apellidos FROM maestros ORDER BY nombres"
    resultado = obtenerDatosDB_Varios(sql)
    return resultado

def obtenerUsuario(vale, ncontrol):
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