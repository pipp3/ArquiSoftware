import json
from time import sleep

"""
@   Manejo de comentarios
*   Este servicio recibe un JSON con las opciones que desea realizar el usuario, ya que es un CRUD.
*   'leer' para leer, 'crear' para insertar, 'borrar' para borrar, 'actualizar' para actualizar.
*   Por cada opción puede que existan diferentes opciones, debido a los campos que tiene cada tabla.
"""
def create(sock, service, msg):
    """
    @   Función para crear un comentario
    *   Recibe el socket, el servicio y el mensaje.
    *   Realiza una validación de los campos que se deben enviar.
    *   Realiza una consulta a la base de datos para insertar el comentario.
    """
    fields: dict = msg['crear']

    if 'fecha' and 'rut_medico' and 'rut_paciente' and "bloque_horario_id" and "motivo" not in fields:
        return incode_response(service, {
            "data": "Incomplete user fields"
        })
    check_sql = {
        "sql": """
            SELECT COUNT(*) AS total
            FROM citas
            WHERE bloque_horario_id = :bloque_horario_id
              AND fecha = :fecha
              AND rut_medico = :rut_medico
              AND estado = 'reservado';
        """,
        "params": {
            "bloque_horario_id": fields['bloque_horario_id'],
            "fecha": fields['fecha'],
            "rut_medico": fields['rut_medico']
        }
    }
    availability_check = process_db_request(sock, check_sql)

  

    # Verifica si el resultado es una lista
    if isinstance(availability_check, list):
        # Si la lista tiene elementos, tomamos el primer elemento
        if len(availability_check) > 0 and 'total' in availability_check[0]:
            total_reservations = int(availability_check[0]['total'])  # Convertir a entero
        else:
            total_reservations = 0
    # Si no es una lista, asumimos que es un diccionario con una estructura distinta
    elif isinstance(availability_check, dict) and 'data' in availability_check:
        print(f"Valor de total_reservations antes de conversión: {availability_check}")

        total_reservations = int(availability_check['data'].get('total', 0))  # Convertir a entero
    else:
        # Caso inesperado, manejamos como un error
        total_reservations = 0

    # Validamos si el bloque está reservado
    if total_reservations > 0:
        return incode_response(service, {
            "data": "El bloque seleccionado ya está reservado. Intente con otro."
        })
    # Registrar la cita
   # Insertar la cita en la base de datos
    insert_sql = {
        "sql": """
            INSERT INTO citas (bloque_horario_id, rut_paciente, rut_medico, motivo, estado, fecha)
            VALUES (:bloque_horario_id, :rut_paciente, :rut_medico, :motivo,:estado, :fecha);
        """,
        "params": {
            "bloque_horario_id": fields['bloque_horario_id'],
            "rut_paciente": fields['rut_paciente'],
            "rut_medico": fields['rut_medico'],
            "motivo": fields['motivo'],
            "fecha": fields['fecha'],
            "estado": "reservado"
        }
    }
    insert_result = process_db_request(sock, insert_sql)

    if len(insert_result) > 0:
        return incode_response(service, {
            "data": "Cita agendada con éxito."
        })
    else:
        return incode_response(service, {
            "data": "Hubo un error al agendar la cita. Intente nuevamente."
        })
    
def read(sock, service, msg):
    """
    @   Función para leer los comentarios
    *   Recibe el socket, el servicio y el mensaje.
    *   Realiza una consulta a la base de datos para obtener los comentarios.
    """
    if msg['leer'] == 'some':

    
        query_sql = {
        "sql": """
            SELECT bh.id AS bloque_id, bh.hora_inicio, bh.hora_fin
            FROM bloque_horario bh
            LEFT JOIN citas c
            ON bh.id = c.bloque_horario_id
            AND c.rut_medico = :rut_medico 
            AND c.fecha = :fecha
            WHERE c.estado IS NULL 
            OR c.estado = 'cancelado';
        """,
        "params": {
            "rut_medico": msg['rut_medico'],
            "fecha": msg['fecha']
        }
    }
        query_result = process_db_request(sock, query_sql)
        if len(query_result)==0:
            return incode_response(service, {
                "data": "No hay bloques disponibles para la fecha y médico seleccionados."
            })
        
        else:
            return incode_response(service, {
                "data": query_result
            })

def update(sock, service, msg):
    """
    @   Función para actualizar un comentario
    *   Recibe el socket, el servicio y el mensaje.
    *   Realiza una validación de los campos que se deben enviar.
    *   Realiza una consulta a la base de datos para actualizar el comentario.
    """
    fields: dict = msg['actualizar']

    if 'id' not in fields:
        return incode_response(service, {
            "data": "Incomplete user fields"
        })

    update_sql = {
        "sql": """
            UPDATE citas
            SET estado = 'completada'
            WHERE id = :id;
        """,
        "params": {
            "id": fields['id']
        }
    }
    update_result = process_db_request(sock, update_sql)

    if len(update_result) > 0:
        return incode_response(service, {
            "data": "Cita marcada como atendida."
        })
    else:
        return incode_response(service, {
            "data": "Hubo un error al marcar la cita como atendida. Intente nuevamente."
        })

def process_request(sock, data):
    """
    @   Función para procesar los mensajes que llegan al servicio
    *   Utiliza la función decoded_data para obtener los valores importantes del mensaje.
    """
    decoded_data = decode_response(data)
    service = decoded_data['service']
    response = json.dumps(decoded_data['data'])

    if service != 'sched':
        return incode_response(service, {
            "data": "Invalid Service: " + service
        })

    try:
        msg = json.loads(response)
        if 'leer' in msg:
            return read(sock=sock, service=service, msg=msg)
        elif 'crear' in msg:
            return create(sock=sock, service=service, msg=msg)
        elif 'actualizar' in msg:
            return update(sock=sock, service=service, msg=msg)
        else:
            return incode_response(service, {
                "data": "No valid options."
            })
    except Exception as err:
        return incode_response(service, {
            "data": "Comment Error: " + str(err)
        })
    
def main(sock, data):
    try:
        return process_request(sock=sock, data=data)
    except Exception as e:
        print("Exception: ", e)
        sleep(20)
        main(sock, data)

if __name__ == "__main__":
    """
    @   Función main
    *   Queda en un loop infinito donde recibe mensajes y los procesa.
    """
    from service import main_service, decode_response, incode_response, process_db_request

    main_service('sched', main)  # Use "usrmn" as the service