import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="config/.env")

def conexion():
    """
    Establece y retorna una conexión a la base de datos MySQL usando variables de entorno.
    """
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    return conn

def obtenerDatosDB(sql, data = None):
    """
    Ejecuta una consulta SQL y retorna un único resultado.
    
    Parámetros:
        sql: Consulta SQL a ejecutar.
        data: Datos para consulta parametrizada.
    """
    conn = conexion()
    cursor = conn.cursor()
    if data is None:
        cursor.execute(sql)
    else:
        cursor.execute(sql, data)
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()
    return resultado

def obtenerDatosDB_Varios(sql, data = None):
    """
    Ejecuta una consulta SQL y retorna varios resultados.
    
    Parámetros:
        sql: Consulta SQL a ejecutar.
        data: Datos para consulta parametrizada.
    """
    conn = conexion()
    cursor = conn.cursor()
    if data is None:
        cursor.execute(sql)
    else:
        cursor.execute(sql, data)
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultado

def obtenerDatosDB_VariosSQL(lista):
    """
    Recibe una lista de SQLs, ejecuta cada uno y regresa una lista de resultados.

    Parámetros:
        lista: Lista de consultas SQL a ejecutar.
    """
    conn = conexion()
    cursor = conn.cursor()
    resultados = []
    for sql in lista:
        cursor.execute(sql)
        resultados.append(cursor.fetchall())
    cursor.close()
    conn.close()
    return resultados

def agregarDatosDB_Individual(sql, data = None):
    """
    Ejecuta una consulta SQL y guarda los cambios.
    
    Parámetros:
        sql: Consulta SQL a ejecutar.
        data: Datos para consulta parametrizada.
    """
    conn = conexion()
    cursor = conn.cursor()
    if data is None:
        cursor.execute(sql)
    else:
        cursor.execute(sql, data)
    conn.commit()
    cursor.close()
    conn.close()

def agregarDatosDB_Individual_for(sql, data):
    """
    Ejecuta una operación SQL INSERT/UPDATE para múltiples registros en una transacción.

    Parámetros:
        sql: Consulta SQL parametrizada.
        data: Tupla que contiene una lista de tuplas con los datos a insertar.
    """
    conn = conexion()
    cursor = conn.cursor()
    for item in data[0]:
        info = (item[0], item[1],)
        cursor.execute(sql, info)
    conn.commit()
    cursor.close()
    conn.close()

def agregarDatosDB_Individual_resetear(sql, data):
    """
    Ejecuta una operación restablecer el material, manejando diferentes tipos de datos.
    
    Parámetros:
        sql: Consulta SQL a ejecutar.
        data: Tupla que contiene una lista de materiales con información a guardar.
    """
    conn = conexion()
    cursor = conn.cursor()
    materiales = data[0]
    for item in materiales:
        try:
            float(item[1])
            info = (item[0], 'S/A',)
        except (ValueError, TypeError):
            info = (item[0], item[1],)
        cursor.execute(sql, info)
    conn.commit()
    cursor.close()
    conn.close()

def agregarDatosDB_Individual_resetear_ocupado(sql, data):
    """
    Ejecuta una operación restablecer el material, manejando diferentes tipos de datos.
    
    Parámetros:
        sql: Consulta SQL a ejecutar.
        data: Tupla que contiene una lista de materiales con información a guardar.
    """
    conn = conexion()
    cursor = conn.cursor()
    materiales = data[0]
    for item in materiales:
        info = (item[0], item[1],)
        cursor.execute(sql, info)
    conn.commit()
    cursor.close()
    conn.close()

def agregarDatosDB_Individual_reporte(sql, data):
    """
    Ejecuta una operación SQL para guardar un reporte, manejando diferentes tipos de datos.
    
    Parámetros:
        sql: Consulta SQL a ejecutar.
        data: Tupla que contiene una lista de materiales con información a guardar.
    """
    conn = conexion()
    cursor = conn.cursor()
    materiales = data[0]
    for item in materiales:
        try:
            float(item[1])
            info = (item[2], 'DISPONIBLE', item[0], 'S/A',)
        except (ValueError, TypeError):
            info = (item[2], 'NO DISPONIBLE', item[0], item[1],)
        cursor.execute(sql, info)
    conn.commit()
    cursor.close()
    conn.close()

def obtenerDatosDB_Varios_Descarga(sql, data = None):
    """
    Ejecuta una consulta SQL y retorna varios resultados, diseñado para operaciones de descarga.
    
    Parámetros:
        sql: Consulta SQL a ejecutar.
        data: Datos para consulta parametrizada.
    """
    conn = conexion()
    cursor = conn.cursor()
    if data is None:
        cursor.execute(sql)
    else:
        cursor.execute(sql, data)
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultado