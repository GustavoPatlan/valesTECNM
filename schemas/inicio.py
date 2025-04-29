import string, random, re
from flask_mail import Mail, Message
from flask import Flask

# Lista de carreras profesionales disponibles en el instituto.
carreras_disponibles = [
    "Ingeniería Biomédica",
    "Ingeniería Bioquímica",
    "Ingeniería Electrónica",
    "Ingeniería Eléctrica",
    "Ingeniería Industrial",
    "Ingeniería Mecatrónica",
    "Ingeniería Mecánica",
    "Ingeniería en Gestión Empresarial",
    "Ingeniería en Materiales",
    "Ingeniería en Semiconductores",
    "Ingeniería en Sistemas Computacionales",
    "Ingeniería en Tecnologías de la Información y Comunicaciones",
    "Licenciatura en Administración",
    "Licenciatura en Contaduría",
]

# Configuración inicial de la aplicación Flask.
app = Flask(__name__)

# Clave secreta para manejar sesiones seguras.
app.secret_key = 'valestecnm'

# Configuración del servicio de correo electrónico (Gmail SMTP).
app.config["MAIL_SERVER"] = "smtp.gmail.com"  # Servidor SMTP de Gmail.
app.config["MAIL_PORT"] = 587  # Puerto para TLS.
app.config["MAIL_USE_TLS"] = True  # Habilitar TLS (seguridad).
app.config["MAIL_USE_SSL"] = False  # No usar SSL (TLS es suficiente).
app.config["MAIL_USERNAME"] = "tecnmvaleselectronicos@gmail.com"  # Cuenta de correo.
app.config["MAIL_PASSWORD"] = "wznm iiwn ineu lrkh"  # Contraseña/App Password.

# Inicialización de la extensión Flask-Mail
mail = Mail(app)

def validar_correo(correo, identificador):
    """
    Valida que un correo electrónico cumpla con el formato institucional requerido.
    
    Parámetros:
        correo: Dirección de correo a validar.
        identificador: Número de control o ID del usuario para validar.
        
    Resultado:
        bool: True si el correo es válido, False si no cumple los requisitos.
    
    Validaciones realizadas:
        Opcionalmente comienza con una letra.
        Puede contener números.
        Debe incluir el identificador proporcionado.
        Dominio exacto: @morelia.tecnm.mx.
    
    Patrón compuesto:
        ^[a-zA-Z]?  -> Letra opcional al inicio.
        [0-9]*       -> Cualquier cantidad de números.
        {identificador} -> El ID debe aparecer completo.
        @morelia\.tecnm\.mx$ -> Dominio institucional exacto.
    """
    patron = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    patron = rf"^[a-zA-Z]?[0-9]*{re.escape(identificador)}@morelia\.tecnm\.mx$"
    return re.match(patron, correo) is not None

def generar_codigo(longitud=6):
    """
    Genera un código aleatorio alfanumérico de la longitud especificada.
    
    Parámetros:
        longitud: Longitud del código a generar. Por defecto es 6.
        
    Resultado:
        string: Código aleatorio que combina letras (mayúsculas/minúsculas) y dígitos.
    
    Características:
        - Usa todos los caracteres ASCII (a-z, A-Z) y dígitos (0-9)
        - Es seguro para códigos de verificación temporales
    """
    caracteres = string.ascii_letters + string.digits
    return "".join(random.choice(caracteres) for _ in range(longitud))

def mandar_correo(patron, correo):
    """
    Envía un correo electrónico con un código de confirmación al destinatario especificado.
    
    Parámetros:
        patron: Código de verificación generado.
        correo: Dirección de correo electrónico del destinatario.
    """
    with app.app_context():
        # Configuración del mensaje.
        asunto = "Código de Confirmación"
        mensaje = f"Tu código de confirmación es: {patron}"

        # Creación del objeto Message.
        msg = Message(asunto, sender=app.config["MAIL_USERNAME"], recipients=[correo])
        msg.body = mensaje

        # Envío del correo.
        mail.send(msg)