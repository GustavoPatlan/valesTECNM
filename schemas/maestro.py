from datetime import datetime
import pytz

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
    zona = pytz.timezone('America/Mexico_City')
    ahora = datetime.now(zona)
    fecha = ahora.strftime('%d/%m/%Y')
    hora = ahora.strftime('%I:%M')
    periodo = 'AM' if ahora.hour < 12 else 'PM'
    hora_con_periodo = f"{hora} {periodo}"
    datos = [fecha, hora_con_periodo]
    print(datos)
    return datos

def crear_identificacion(ncontrol, horarios):
    """
    Genera un ID único para solicitudes de maestros combinando:
    - Prefijo 'M'.
    - Número de control.
    - Hora actual.
    - Fecha actual.
    """
    identificacion = 'M' + ncontrol + horarios[1].replace(" ", "").replace(":", "") + horarios[0].replace("/", "") 
    return identificacion