import os
import socket
import sys
import json
from dotenv import load_dotenv


load_dotenv()


def send_message(sock, message):
    """
    @   Enviar mensaje al socket
    *   Se asume que el mensaje fue codificado previamente a enviar usando incode_response
    """
    sock.sendall(message)


def receive_message(sock, expected_length):
    """
    @   Recibir mensaje
    *   Calcula el tamaño del mensaje de acuerdo al bus y lee los datos
    """
    received_data = b''
    while len(received_data) < expected_length:
        data = sock.recv(expected_length - len(received_data))
        if not data:
            raise RuntimeError("Socket connection closed prematurely.")
        received_data += data
    return received_data


def decode_response(response):
    """
    @   Decodificar mensajes de los clientes
    *   Por alguna razón hay veces donde se envía con el largo del mensaje y otras veces que no.
    *   Por tanto se revisa esos casos y se retorna un diccionario con 'length', 'status' y 'data'
    *   Data corresponde al JSON que envía el cliente.
    """
    response = response.decode('utf-8')
    try:
        length = int(response[:5])
        service = response[5:10]
        response_data = json.loads(response[10:])
        if response[5:7] == 'OK' or response[5:7] == 'NK':
            service = response[7:12]
            response_data = json.loads(response[12:])
        return {
            "length": length,
            "service": service,
            "data": response_data
        }
    except ValueError:
        service = response[:5]
        response_data = json.loads(response[5:])
        if response[5:7] == 'OK' or response[5:7] == 'NK':
            service = response[7:12]
            response_data = json.loads(response[12:])
        return {
            "length": 0,
            "service": service,
            "data": response_data
        }


def incode_response(service, response):
    """
    @   Codificar mensaje hacia el cliente
    *   Enviamos un JSON codificado en bytes que sigue el patrón de mensaje del bus.
    """
    data_json = json.dumps(response)
    msg_len = len(service) + len(data_json)
    response_formatted = f'{msg_len:05d}{service}{data_json}'
    return response_formatted.encode('utf-8')


def is_sinit_response(response):
    """
    @   Revisamos respuesta de SInit
    *   Esto es para poder saltar un mensaje adicional que no era necesario.
    """
    response = response.decode('utf-8')
    if response[:5] == 'sinit':
        return True
    return False


def process_db_request(sock, sql):
    """
    @   Conexión al servicio de BDD
    *   Esta función recibe una query SQL con la cuál se conecta a la bdd usando el servicio DBCON.
    *   Por tanto, para poder ejecutar es necesario tener corriendo el servicio de DBCON.
    """
    try:
        #   Hacemos el request al servicio 'dbcon' igual que con cualquier otro servicio
        db_request = incode_response('dbcon', sql)
        print(f'Requesting data from db: {db_request}')
        send_message(sock, db_request)
        print(f'Waiting for response...')
        expected_length = int(receive_message(sock, 5).decode('utf-8'))
        received_data = receive_message(sock, expected_length)
        print(f'Received data: {received_data}')

        #   Los datos se encuentran en bytes, es necesario codificar los datos
        db_data = json.loads(received_data[7:])
        format_db_data = incode_response('dbcon', db_data)
        decode_db_data = decode_response(format_db_data)
        #   Retornamos los datos codificados
        if isinstance(decode_db_data['data'], str):
            return decode_db_data['data']
        else:
            return decode_db_data['data']['data']
    except Exception as err:
        return {
            "data": "Error de Process DB Request: " + str(err)
        }


def user_id_request(sock, datos):
    """
    @   Conexión al servicio de Usuario
    *   Esta función recibe un JSON { "leer": "some", "usuario": "hola" }
    *   Retorna un 'ID' de usuario como STRING.
    """
    try:
        #   Hacemos el request al servicio 'dbcon' igual que con cualquier otro servicio
        usr_request = incode_response('usrmn', datos)
        print(f'Requesting data from User Service: {usr_request}')
        send_message(sock, usr_request)
        print(f'Waiting for response...')
        expected_length = int(receive_message(sock, 5).decode('utf-8'))
        received_data = receive_message(sock, expected_length)
        print(f'Received data: {received_data}')

        #   Los datos se encuentran en bytes, es necesario codificar los datos
        request_data = json.loads(received_data[7:])
        format_request_data = incode_response('usrmn', request_data)
        decode_request_data = decode_response(format_request_data)
        #   Retornamos los datos codificados
        if isinstance(decode_request_data['data']['data'], str):
            return decode_request_data['data']['data']
        else:
            return decode_request_data['data']['data']['data']
    except Exception as err:
        return {
            "data": "User Management Service Error: " + str(err)
        }


def get_user_id(sock, usuario):
    """
    @   Obtener ID de Usuario
    *   Esta función retorna el ID del usuario como STR, sino retorna None.
    """
    db_sql = {
        "sql": "SELECT id FROM usuario WHERE usuario = :usuario",
        "params": {
            "usuario": usuario,
        }
    }
    db_request: list = process_db_request(sock, db_sql)
    if len(db_request) == 0:
        return None
    else:
        return db_request[0]['id']


def main_service(service, process_request):
    """
    @   Servicio principal
    *   Todos los servicios deben tener esta función para ser servicio. Se conecta al bus en localhost y puerto 5000.
    *   Envia un mensaje de 'sinit' para poder iniciar el servicio dentro del bus.
    *   Luego, se queda en un loop infinito esperando transacciones.
    *   Cuando llega una transaccion, es procesada por la función 'process_request' de cada servicio.
    *   El resultado del procesamiento lo decodificamos para posteriormente codificarlo y enviarlo.
    """
    server_address = (f"{os.getenv('SOABUS_HOST')}", 5000)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect(server_address)

            message = bytes(f'00010sinit{service}', 'utf-8')
            print(f'Sending message: {message}')
            send_message(sock, message)

            while True:
                print('Waiting for transaction...')
                expected_length = int(receive_message(sock, 5).decode('utf-8'))
                data = receive_message(sock, expected_length)
                print(f'Received data: {data}')

                if is_sinit_response(data):
                    continue

                print('Processing...')
                response = process_request(sock=sock, data=data)
                decoded = decode_response(response)
                response = incode_response(decoded['service'], decoded['data'])
                print(f'Sending response: {response}')
                send_message(sock, response)
        except KeyboardInterrupt:
            print(f'Terminating service {service}')
            sock.close()
            sys.exit(0)
        finally:
            sock.close()
            sys.exit(0)