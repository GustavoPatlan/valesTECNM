import mysql.connector

def conexion():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="vales"
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
    conn = conexion()
    cursor = conn.cursor()
    for item in data[0]:
        info = (item[0], item[1],)
        cursor.execute(sql, info)
    conn.commit()
    cursor.close()
    conn.close()

def agregarDatosDB_Individual_reporte(sql, data):
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

def material_lab():
    conn = conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT EQUIPO, N_CASETA, NUMERACION FROM labpotencia WHERE disponibilidad = 'DISPONIBLE'")
    myresult = cursor.fetchall()
    pot = [(elem + ('POT',) if 'POT' not in elem else elem) for elem in myresult]
    cursor.execute("SELECT EQUIPO, N_CASETA, NUMERACION FROM labelectronica WHERE disponibilidad = 'DISPONIBLE'")
    myresult = cursor.fetchall()
    ad = [(elem + ('A/D',) if 'A/D' not in elem else elem) for elem in myresult]
    cursor.execute("SELECT EQUIPO, N_CASETA, NUMERACION FROM labthird WHERE disponibilidad = 'DISPONIBLE'")
    myresult = cursor.fetchall()
    sd = [(elem + ('S/D',) if 'S/D' not in elem else elem) for elem in myresult]
    all_results = pot + ad + sd
    conn.commit()
    cursor.close()
    conn.close()
    return all_results