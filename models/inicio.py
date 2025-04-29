from config.database import *

def usuarioInicio(identificador, usuario='Estudiante'):
    """
    Obtiene información de usuario según su tipo de rol.
    
    Parámetros:
        identificador: Número de control o ID del usuario.
        usuario: Tipo de rol ('Estudiante', 'Maestro', 'Casetero', 'Admin').
            Valor por defecto: 'Estudiante'.
    
    Resultado:
        resultado: Datos del usuario si existe, None si no se encuentra.
    """
    match usuario:
        case 'Estudiante':
            sql = "SELECT * FROM usuarios WHERE ncontrol = %s"  # Busca en tabla de usuarios.
        case 'Maestro':
            sql = "SELECT * FROM maestros WHERE id = %s" # Busca en tabla de maestros.
        case 'Casetero':
            sql = "SELECT * FROM caseteros WHERE id = %s" # Busca en tabla de caseteros.
        case 'Admin':
            sql = "SELECT * FROM administrador WHERE id = %s" ## Busca en tabla administrador.
    data = (identificador,)
    resultado = obtenerDatosDB(sql, data)
    return resultado

def obtenerEstudianteDB(correo):
    """
    Consulta un estudiante en la base de datos usando su correo electrónico.

    Parámetros:
        correo: Correo electrónico institucional del estudiante a buscar.

    Resultado:
        resultado: Datos del usuario si existe, None si no se encuentra.
    """
    sql = "SELECT * FROM usuarios WHERE correo = %s"
    data = (correo,)
    resultado = obtenerDatosDB(sql, data)
    return resultado

def actualizarLlaveEstudianteDB(llave, correo):
    """
    Actualiza la contraseña de un estudiante en la base de datos.

    Parámetros:
        llave: Nueva contraseña.
        correo: Correo electrónico del estudiante.
    """
    sql = "UPDATE usuarios SET llave = %s WHERE correo = %s"
    data = (llave, correo,)
    agregarDatosDB_Individual(sql, data)

def registrarEstudianteDB(identificador, correo, carrera, nombre, apellido, llave):
    """
    Registra un nuevo estudiante en la base de datos con los datos proporcionados.

    Parámetros:
        identificador: Número de control del estudiante.
        correo: Correo institucional del estudiante.
        carrera: Carrera a la que pertenece el estudiante.
        nombre: Nombre(s) del estudiante.
        apellido: Apellido(s) del estudiante.
        llave: Contraseña del estudiante.

    Campos adicionales establecidos por defecto:
        - laboratorio: '0' (valor inicial).
        - proyecto: '0' (valor inicial).
    """
    sql = '''INSERT INTO usuarios 
                (ncontrol, laboratorio, proyecto, correo, carrera, nombres, apellidos, llave) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''
    data = (identificador, '0', '0', correo, carrera, nombre, apellido, llave,)
    agregarDatosDB_Individual(sql, data)