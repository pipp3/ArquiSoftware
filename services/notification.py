import json
from time import sleep
from twilio.rest import Client
from dotenv import load_dotenv
import os

"""
@   Manejo de Notificaciones
*   Este servicio recibe un JSON con las opciones que desea realizar el usuario, ya que es un CRUD.
*   'leer' para leer, 'crear' para insertar.
*   Por cada opción puede que existan diferentes opciones, debido a los campos que tiene cada tabla.
"""

load_dotenv()

def create(sock, service, msg):
    print(f"Account SID: {os.getenv('TWILIO_ACCOUNT_SID')}")
    print(f"Auth Token: {os.getenv('TWILIO_AUTH_TOKEN')}")
    """
    Función para leer los datos de la tabla y enviar notificaciones.
    """
    fields: dict = msg['crear']
    if 'cita_id' not in fields or 'mensaje' not in fields or 'destino' not in fields:
        return incode_response(service, {
            "data": "Incomplete user fields"
        })
    

    # Insertar la notificación en la base de datos
    db_sql = {
        "sql": "INSERT INTO notificaciones (cita_id, mensaje, fecha) VALUES (:cita_id, :mensaje, CURRENT_TIMESTAMP)",
        "params": {
            "cita_id": fields['cita_id'],
            "mensaje": fields['mensaje']
        },
    }
    db_request = process_db_request(sock, db_sql)
    if len(db_request) > 0:
        try:
            celular=fields['destino']
            client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
            # Enviar SMS al número de celular proporcionado
            message = client.messages.create(
                from_='+12029726553',  # Asegúrate de usar un número válido
                body=fields['mensaje'],
                to=f'+56{celular}'  # Suponiendo que el número está en formato chileno
            )
            print(f"Mensaje enviado: {message.sid}")  # Imprimir el SID del mensaje para verificar
            return incode_response(service, {
                "data": f"Se insertó la notificación y se envió el mensaje correctamente."
            })
        except Exception as e:
            # Imprimir el error completo para más detalles
            print(f"Error al enviar el mensaje: {str(e)}")
            return incode_response(service, {
                "data": f"Notificación enviada, pero ocurrió un error al enviar el SMS: {str(e)}"
            })
    else:
        return incode_response(service, {
            "data": "Error sending notification"
        })
    
            

def read(sock,service,msg):
    """
    @   Función para leer los datos de la tabla
    *   Recibe el socket, el servicio y el mensaje.
    *   Si el mensaje es 'some' se leerán los registros que cumplan con los campos del mensaje.
    """
    if msg["leer"]=="all":
        
            db_sql={
                "sql":"SELECT * FROM notificaciones ORDER BY id DESC LIMIT 5",
            }
            db_request=process_db_request(sock,db_sql)
            if(len(db_request)==0):
                return incode_response(service,{
                    "data":"No notifications found."
                })
            else:
                return incode_response(service,{
                    "data":db_request
                })
        
    elif msg["leer"]=="some":
        if "id" in msg:
            db_sql={
                "sql":"SELECT * FROM notificaciones WHERE id=:id",
                "params":{
                    "id":msg["id"]
                }
            }
            db_request=process_db_request(sock,db_sql)
            if(len(db_request)==0):
                return incode_response(service,{
                    "data":"No notifications found."
                })
            else:
                return incode_response(service,{
                    "data":db_request
                })
        elif "rut_paciente" in msg:
            db_sql={
                "sql":"SELECT n.id, n.mensaje, n.fecha FROM notificaciones n JOIN citas c ON n.cita_id = c.id WHERE c.rut_paciente = :rut_paciente ORDER BY n.fecha DESC LIMIT 5;",
                "params":{
                    "rut_paciente":msg["rut_paciente"]
                }
            }
            db_request=process_db_request(sock,db_sql)
            if(len(db_request)==0):
                return incode_response(service,{
                    "data":"No notifications found."
                })
            else:
                return incode_response(service,{
                    "data":db_request
                })
        elif "rut_medico" in msg:
            db_sql={
                "sql":"SELECT n.id, n.mensaje, n.fecha FROM notificaciones n JOIN citas c ON n.cita_id = c.id WHERE c.rut_medico = :rut_medico ORDER BY n.fecha DESC LIMIT 5;",
                "params":{
                    "rut_medico":msg["rut_medico"]
                }
            }
            db_request=process_db_request(sock,db_sql)
            if(len(db_request)==0):
                return incode_response(service,{
                    "data":"No notifications found."
                })
            else:
                return incode_response(service,{
                    "data":db_request
                })
        
        elif "cita_id" in msg:
            db_sql={
                "sql":"SELECT * FROM notificaciones WHERE cita_id=:cita_id",
                "params":{
                    "cita_id":msg["cita_id"]
                }
            }
            db_request=process_db_request(sock,db_sql)
            if(len(db_request)==0):
                return incode_response(service,{
                    "data":"No notifications found."
                })
            else:
                return incode_response(service,{
                    "data":db_request
                })
        
        elif "rut" and "id_noti" in msg:
            db_sql = {
                "sql": """
                    WITH usuario_tipo AS (
                        SELECT 'paciente' AS tipo
                        FROM pacientes
                        WHERE rut = :rut
                        UNION ALL
                        SELECT 'medico' AS tipo
                        FROM funcionarios
                        WHERE rut = :rut
                    )
                    SELECT n.id, n.mensaje, n.fecha
                    FROM notificaciones n
                    JOIN citas c ON n.cita_id = c.id
                    WHERE n.id = :id_noti
                    AND (c.rut_paciente = :rut OR c.rut_medico = :rut);
                """,
                "params": {
                    "rut": msg["rut"],
                    "id_noti": msg["id_noti"]
                }
            }
            db_request=process_db_request(sock,db_sql)
            if(len(db_request)==0):
                return incode_response(service,{
                    "data":"No se encontro la notificacion para su usuario."
                })
            else:
                return incode_response(service,{
                    "data":db_request
                })
        elif "rut" in msg:
            db_sql = {
                "sql": """
                    WITH usuario_tipo AS (
                        SELECT 'paciente' AS tipo
                        FROM pacientes
                        WHERE rut = :rut
                        UNION ALL
                        SELECT 'medico' AS tipo
                        FROM funcionarios
                        WHERE rut = :rut
                    )
                    SELECT n.id, n.mensaje, n.fecha
                    FROM notificaciones n
                    JOIN citas c ON n.cita_id = c.id
                    WHERE c.rut_paciente = :rut OR c.rut_medico = :rut
                    ORDER BY n.fecha DESC
                    LIMIT 5;
                """,
                "params": {
                    "rut": msg["rut"]
                    }
                }
            db_request=process_db_request(sock,db_sql)
            if(len(db_request)==0):
                return incode_response(service,{
                    "data":"No notifications found."
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

    if service != 'notif':
        return incode_response(service, {
            "data": "Invalid Service: " + service
        })

    try:
        msg = json.loads(response)
        if 'leer' in msg:
            return read(sock=sock, service=service, msg=msg)
        elif 'crear' in msg:
            return create(sock=sock, service=service, msg=msg)
      
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

    main_service('notif', main) 