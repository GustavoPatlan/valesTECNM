from flask import Flask
from flask_socketio import SocketIO
from dotenv import load_dotenv
import os

from routes.inicio import rutasDeInicio
from routes.estudiantes import rutasDeEstudiantes
from routes.maestro import rutasDeMaestro
from routes.casetero import rutasDeTrabajador

load_dotenv(dotenv_path="config/.env")

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")
socketio = SocketIO(app, cors_allowed_origins="*")

rutasDeInicio(app)
rutasDeEstudiantes(app, socketio)
rutasDeMaestro(app, socketio)
rutasDeTrabajador(app, socketio)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)