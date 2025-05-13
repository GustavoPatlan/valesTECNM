from flask import Flask
from dotenv import load_dotenv
import os

from routes.inicio import rutasDeInicio
from routes.estudiantes import rutasDeEstudiantes
from routes.maestro import rutasDeMaestro
from routes.casetero import rutasDeTrabajador
from routes.administrador import rutasDeAdministrador

load_dotenv(dotenv_path="config/.env")

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

rutasDeInicio(app)
rutasDeEstudiantes(app)
rutasDeMaestro(app)
rutasDeTrabajador(app)
rutasDeAdministrador(app)

if __name__ == '__main__':
    app.run(debug=True)