import json
from time import sleep
from utils.passwords import verify_password
"""
@   Manejo de usuarios
*   Este servicio recibe un JSON con las opciones que desea realizar el usuario, ya que es un CRUD.
*   'leer' para leer, 'crear' para insertar, 'borrar' para borrar, 'actualizar' para actualizar.
*   Por cada opción puede que existan diferentes opciones, debido a los campos que tiene cada tabla.
"""


def login(sock, service, msg):
    """
    @   Función para insertar un usuario en la tabla usuario
    *   Recibe un diccionario en "crear", el cual debe incluir todos los campos de usuario requeridos.
    *   Ejemplo:    "login" : { "usuario": "hola", "password": "hola" }
    """
    #   Opción de crear usuarios
    fields: dict = msg['login']
    if 'usuario' and 'password' not in fields:
        return incode_response(service, {
            "data": "Incomplete user fields."
        })
    db_sql = {
        "sql": "SELECT id,usuario,nombre,cargo,area,password FROM usuarios WHERE usuario = :usuario",
        "params": {
            "usuario": fields['usuario']
        }
    }
    db_request = process_db_request(sock, db_sql)

    if not db_request:
        datos = {
            "id": "",
            "usuario": "",
            "cargo": "",
            "area": "",
            "autenticado": "false",
        }
        return incode_response(service, {
            "data": datos
        })
    
    user_data = db_request[0]
    stored_password_hash = user_data['password']

    # Verificamos la contraseña
    if verify_password(fields['password'], stored_password_hash):
        datos = {
            "id": user_data['id'],
            "usuario": user_data['usuario'],
            "cargo": user_data['cargo'],
            "area": user_data['area'],
            "autenticado": "true",
        }
        return incode_response(service, {
            "data": datos
        })
    else:
        datos = {
            "id": "",
            "usuario": "",
            "cargo": "",
            "area": "",
            "autenticado": "false",
        }
        return incode_response(service, {
            "data": datos
        })

def process_request(sock, data):
    """
    @   Función para procesar los mensajes que llegan al servicio
    *   Utiliza la función decoded_data para obtener los valores importantes del mensaje.
    """
    decoded_data = decode_response(data)
    service = decoded_data['service']
    response = json.dumps(decoded_data['data'])

    if service != 'usrlg':
        return incode_response(service, {
            "data": "Invalid Service: " + service
        })

    try:
        msg = json.loads(response)
        if 'login' in msg:
            return login(sock=sock, service=service, msg=msg)
        else:
            return incode_response(service, {
                "data": "No valid options."
            })
    except Exception as err:
        return incode_response(service, {
            "data": "User Login Error: " + str(err)
        })


def main(sock, data):
    try:
        return process_request(sock=sock, data=data)
    except Exception as e:
        print("Exception: ", e)
        sleep(5)
        main(sock, data)


if __name__ == "__main__":
    """
    @   Función main
    *   Queda en un loop infinito donde recibe mensajes y los procesa.
    """
    from service import main_service, decode_response, incode_response, process_db_request

    main_service('usrlg', main)  # Use "usrmn" as the service