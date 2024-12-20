import json
from time import sleep

def actualiza_cita(sock, service, msg):
    """
    @   Función actualiza_cita
    *   Función para actualizar una cita.
    """


    if msg["actualizar"] == "some":
        # Realizar la actualización de la cita en la base de datos
        db_sql = {
            "sql": """
                UPDATE citas
                SET fecha = :fecha,
                bloque_horario_id = :bloque_horario_id
                WHERE id = :cita_id
                AND estado != 'cancelado'
                AND estado != 'completada';
            """,
            "params": {
                "cita_id": msg['cita_id'],
                "fecha": msg['fecha'],
                "bloque_horario_id": msg['bloque_horario_id']
            }
        }
        db_request = process_db_request(sock, db_sql)
        if len(db_request) == 0:
            return incode_response(service, {
                "data": "No se encontró la cita"
            })
        else:
            return incode_response(service, {
                "data": "Cita re-agendada con éxito"
            })
def read(sock, service, msg):
    """
    @   Función para leer las citas de un paciente.
    """
    if msg["leer"]=="some" and 'rut_paciente' in msg:
        db_sql = {
            "sql": """
                SELECT 
                    c.id AS cita_id,
                    c.rut_medico,
                    c.rut_paciente,
                    bh.hora_inicio,
                    bh.hora_fin,
                    c.motivo AS motivo,
                    c.estado,
                    c.fecha
                FROM 
                    citas c
                JOIN 
                    bloque_horario bh
                ON 
                    c.bloque_horario_id = bh.id
                WHERE 
                    c.rut_paciente = :rut_paciente
                    AND c.estado != 'cancelado'
                    AND c.estado != 'completada';

            """,
            "params": {
                "rut_paciente": msg['rut_paciente']
            }
        }
        db_request = process_db_request(sock, db_sql)
        if len(db_request) == 0:
            return incode_response(service, {
                "data": "No se encontraron citas"
            })
        else:
            return incode_response(service, {
                "data": db_request
            })
    elif msg["leer"]=="some" and 'rut_medico' in msg:
        db_sql = {
            "sql": """
                SELECT 
                    c.id AS cita_id,
                    c.rut_medico,
                    c.rut_paciente,
                    bh.hora_inicio,
                    bh.hora_fin,
                    c.motivo AS motivo,
                    c.estado,
                    c.fecha
                FROM 
                    citas c
                JOIN 
                    bloque_horario bh
                ON 
                    c.bloque_horario_id = bh.id
                WHERE 
                    c.rut_medico = :rut_medico
                    AND c.estado != 'cancelado'
                    AND c.estado != 'completada';

            """,
            "params": {
                "rut_medico": msg['rut_medico']
            }
        }
        db_request = process_db_request(sock, db_sql)
        if len(db_request) == 0:
            return incode_response(service, {
                "data": "No se encontraron citas"
            })
        else:
            return incode_response(service, {
                "data": db_request
            })
    

def process_request(sock, data):
    """
    @   Función para procesar los mensajes que llegan al servicio
    *   Utiliza la función decoded_data para obtener los valores importantes del mensaje.
    """
    decoded_data = decode_response(data)
    service = decoded_data['service']
    response = json.dumps(decoded_data['data'])

    if service != 'resch':
        return incode_response(service, {
            "data": "Invalid Service: " + service
        })

    try:
        msg = json.loads(response)
        if 'actualizar' in msg:
            return actualiza_cita(sock=sock, service=service, msg=msg)
        if 'leer' in msg:
            return read(sock=sock, service=service, msg=msg)

        else:
            return incode_response(service, {
                "data": "No valid options."
            })
    except Exception as err:
        return incode_response(service, {
            "data": "User Management Error: " + str(err)
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

    main_service('resch', main)  # Use "usrmn" as the service