from datetime import datetime

def compara_y_agrega(list1, list2):
    """
    Combina y enriquece datos de dos listas diferentes, agregando información correspondiente
    desde la segunda lista a la primera.
    """
    structured_list1 = [(list1[i], list1[i+1]) for i in range(0, len(list1), 2)]
    dict_list2 = dict(list2)
    result = []
    for name, quantity in structured_list1:
        third_value = dict_list2.get(name, 'NO')
        result.append((name, quantity, third_value))
    
    return result

def obtener_horario():
    """
    Obtiene la fecha y hora actual del sistema formateadas para visualización.

    Genera:
        - Fecha en formato DD/MM/AAAA.
        - Hora en formato 12 horas con indicador AM/PM.
        - Los datos se retornan como una lista.

    Resultado:
        resultado: Datos del con fecha y hora.
    """
    ahora = datetime.now()
    fecha = ahora.strftime('%d/%m/%Y')
    hora = ahora.strftime('%I:%M')
    periodo = 'AM' if ahora.hour < 12 else 'PM'
    hora_con_periodo = f"{hora} {periodo}"
    datos = [fecha, hora_con_periodo]
    return datos

def crear_identificacion(ncontrol, vale, horarios):
    """
    Genera un identificador único para vales.

    Parámetros:
        ncontrol: Número de control del estudiante.
        vale: Tipo de vale.
        horarios: Lista con fecha y hora.

    Proceso:
        1. Determina el prefijo según tipo de vale:
            - 'P' para vales de PROYECTO.
            - 'L' para otros tipos de vale.
        2. Formatea la hora eliminando espacios y dos puntos.
        3. Formatea la fecha eliminando barras.
        4. Combina todos los componentes en una sola cadena.
    """
    if vale == 'PROYECTO':
        lada = 'P'
    else:
        lada = 'L'
    identificacion = lada + ncontrol + horarios[1].replace(" ", "").replace(":", "") + horarios[0].replace("/", "") 
    return identificacion