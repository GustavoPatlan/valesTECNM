from datetime import datetime

# Obtener fecha y hora actual
def obtener_horario():
    ahora = datetime.now()
    fecha = ahora.strftime('%d/%m/%Y')
    hora = ahora.strftime('%I:%M')
    periodo = 'AM' if ahora.hour < 12 else 'PM'
    hora_con_periodo = f"{hora} {periodo}"
    datos = [fecha, hora_con_periodo]
    return datos

def crear_identificacion(ncontrol, horarios):
    identificacion = 'M' + ncontrol + horarios[1].replace(" ", "").replace(":", "") + horarios[0].replace("/", "") 
    return identificacion