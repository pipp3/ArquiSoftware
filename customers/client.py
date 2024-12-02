import json
import socket
from tabulate import tabulate

"""
@   Archivo principal de cliente
*   Todos los clientes deberán importar las funciones de este archivo.
"""


def send_message(sock, service: str, data: dict):
    """
    @   Enviar Mensaje
    *   Esta función recibe un string indicando el servicio y un diccionario para los datos (JSON).
    *   Luego, se envia siguiendo el formato del bus por el socket.
    """
    try:
        print(f"Preparando mensaje para el servicio: {service}")
        data = json.dumps(data)
        print(f"Datos convertidos a JSON: {data}")
        
        msg_len = len(service) + len(data)
        print(f"Longitud del mensaje: {msg_len}")
        
        message = f"{msg_len:05d}{service}{data}"
        encoded_msg = message.encode('utf-8')
        
        print(f"Mensaje codificado: {encoded_msg}")
        sock.sendall(encoded_msg)
        print(f"Mensaje enviado con éxito.")
        
    except json.JSONDecodeError as json_error:
        print(f'Error decodificando JSON: {json_error}')
        raise RuntimeError('No se pudo decodificar el JSON.')
    except socket.error as sock_error:
        print(f'Error de socket: {sock_error}')
        raise RuntimeError('No se pudo recibir respuesta del socket.')
    except Exception as e:
        print(f'Error inesperado: {e}')
        raise RuntimeError('Ocurrio un error inesperado.')


def receive_response(sock):
    """
    @   Recibir Mensaje
    *   Esta función escucha el socket y recibe los mensajes.
    *   Luego, decodifica los campos de acuerdo al patrón de mensaje del bus.
    *   Finalmente, retorna un JSON con 'status', 'service' y 'data'.
    """
    try:
        print("----------------------------------")
        print("Esperando respuesta del socket...")


        
        response_len = int(sock.recv(5).decode())
        print(f"Longitud de la respuesta: {response_len}")
        
        response_service = sock.recv(5).decode()
        print(f"Servicio recibido: {response_service}")
        
        response_data = sock.recv(response_len - 5).decode()
        print(f"Datos de la respuesta recibidos: {response_data}")
        
        response_status = response_data[:2]
        print(f"Estado de la respuesta: {response_status}")
        
        response_json = json.loads(response_data[2:])
        print(f"Datos decodificados: {response_json}")
        
        return {
            "status": response_status,
            "service": response_service,
            "data": response_json['data']
        }
    
    except (ValueError, json.JSONDecodeError) as json_error:
        print(f'Error decodificando JSON: {json_error}')
        raise RuntimeError('No se pudo decodificar el JSON.')
    except socket.error as sock_error:
        print(f'Error de socket: {sock_error}')
        raise RuntimeError('No se pudo recibir respuesta del socket.')
    except Exception as e:
        print(f'Error inesperado: {e}')
        raise RuntimeError('Ocurrio un error inesperado.')
    


def valid_fields(user_input, max_length):
    if len(user_input) > max_length:
        return False
    if not user_input.isalnum():
        return False
    return True


def input_field(text_input, max_length):
    field = input(text_input)
    while not valid_fields(field, max_length):
        print(f"Error: Los datos no son correctos. Intente un largo máximo de {max_length} carácteres alfanuméricos.")
        field = input(text_input)
    return field.lower()


def valid_id_field(data_list, input_id: str):
    if not input_id.isdigit():
        return False

    id_list = []
    for row in data_list:
        id_list.append(int(row['id']))

    if int(input_id) not in id_list:
        return False

    return True


def input_id_field(text_input, data_list):
    input_id = input(text_input)
    while not valid_id_field(data_list, input_id):
        print(f"Error: El ID ingresado no es correcto.")
        input_id = input(text_input)
    return input_id.lower()


def service_request(sock, service, datos):
    """
    @   Solicitud de Servicio
    *   Envía un mensaje al servicio especificado y espera la respuesta.
    """
    try:
        print("----------------------------------")
        print(f"Preparando solicitud para el servicio: {service}")
        print(f"Datos a enviar: {datos}")
        
        # Enviamos el mensaje mediante el socket al servicio
        send_message(sock, service, datos)
        print("Mensaje enviado exitosamente.")
        
        # Recibimos la respuesta desde el socket
        print("Esperando respuesta del socket...")
        respuesta = receive_response(sock)
        print(f"Respuesta recibida: {respuesta}")
        
        # Retornamos el estado y los datos
        return respuesta['status'], respuesta['data']
    
    except Exception as e:
        print(f"Error durante la solicitud al servicio '{service}': {e}")
        raise



def save_session(data):
    with open('./session.json', 'w') as json_file:
        json.dump(data, json_file, indent=2)


def get_session():
    with open('./session.json', 'r') as json_file:
        data = json.load(json_file)
    return data


def auth_session(session: dict, area):
    if 'id' not in session:
        print('Usuario no autenticado. Por favor inicie sesión.')
        return False
    elif 'area' not in session or session['area'] != area:
        print('No tiene permisos para realizar esta operación.')
        return False
    elif 'autenticado' not in session or session['autenticado'] != 'true':
        return False
    return True


def print_table(data):
    headers = data[0].keys()  # Assuming all dictionaries have the same keys
    table = []

    for item in data:
        table.append([item[key] for key in headers])

    print(tabulate(table, headers=headers, tablefmt='grid'))


def print_select(status, data):
    if status == 'OK':
        if isinstance(data, list):
            print_table(data)
        else:
            print(data)
    else:
        print(f"Ocurrió un error: {data}")


def print_ins_del_upd(status, data):
    if status == 'OK':
        print(data)
    else:
        print(f"Ocurrió un error: {data}")