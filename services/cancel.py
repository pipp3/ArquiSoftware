import json
from time import sleep

def cancel(sock, service, msg):
    """
    @   Función cancel
    *   Función para cancelar una hora.
    """
    fields: dict = msg['cancelar']

     # Verificar que ambos campos (rut_paciente y cita_id) estén presentes
    if 'cita_id' not in fields:
        return incode_response(service, {
            "data": "Incomplete user fields"
        })
     # Realizar la actualización de la cita en la base de datos
    db_sql = {
        "sql": """
            UPDATE citas
            SET estado = 'cancelado' 
            WHERE id = :cita_id
            AND estado != 'cancelado' 
        """,
        "params": {
            "cita_id": fields['cita_id'],
        }
    }
    db_request= process_db_request(sock, db_sql)
    if len(db_request)==0:
        return incode_response(service, {
            "data": "No se encontró la cita"
        })
    else:
        return incode_response(service, {
            "data": "Cita cancelada con éxito"
        })

def read(sock, service, msg):
    """
    @   Función read
    *   Función para leer las horas canceladas.
    """
    fields: dict = msg['leer']

    # Realizar la lectura de las citas canceladas en la base de datos
    if msg['leer'] == 'all':
        db_sql = {
            "sql": """
                SELECT * FROM citas
                WHERE estado = 'cancelado' LIMIT 50
            """,
            "params": {}
        }
        db_request=process_db_request(sock,db_sql)
        if(len(db_request)==0):
            return incode_response(service,{
                "data":"No comments found."
            })
        else:
            return incode_response(service,{
                "data":db_request
            })
    elif msg['leer']=='some':
        if 'rut_paciente' in msg:
            db_sql={
                "sql":"SELECT * FROM citas WHERE rut_paciente=:rut_paciente AND estado='cancelado",
                "params":{
                    "rut_paciente":msg["rut_paciente"]
                }
            }
            db_request=process_db_request(sock,db_sql)
            if(len(db_request)==0):
                return incode_response(service,{
                    "data":"No comments found."
                })
            else:
                return incode_response(service,{
                    "data":db_request
                })
        elif 'rut_medico' in msg:
            db_sql={
                "sql":"SELECT * FROM citas WHERE rut_medico=:rut_medico AND estado='cancelado",
                "params":{
                    "rut_medico":msg["rut_medico"]
                }
            }
            db_request=process_db_request(sock,db_sql)
            if(len(db_request)==0):
                return incode_response(service,{
                    "data":"No comments found."
                })
            else:
                return incode_response(service,{
                    "data":db_request
                })
    else:
        return incode_response(service,{
            "data":"No valid options."
        })
        

    
def process_request(sock, data):
    """
    @   Función para procesar los mensajes que llegan al servicio
    *   Utiliza la función decoded_data para obtener los valores importantes del mensaje.
    """
    decoded_data = decode_response(data)
    service = decoded_data['service']
    response = json.dumps(decoded_data['data'])

    if service != 'cance':
        return incode_response(service, {
            "data": "Invalid Service: " + service
        })

    try:
        msg = json.loads(response)
        if 'leer' in msg:
            return read(sock=sock, service=service, msg=msg)
       
        elif 'cancelar' in msg:
            return cancel(sock=sock, service=service, msg=msg)
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

    main_service('cance', main)  # Use "usrmn" as the service