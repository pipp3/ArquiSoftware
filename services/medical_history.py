import json
from time import sleep

"""
@   Manejo de Historial Médico
*   Este servicio recibe un JSON con las opciones que desea realizar el usuario, ya que es un CRUD.
*   'leer' para leer, 'crear' para insertar, 'borrar' para borrar, 'actualizar' para actualizar.
*   Por cada opción puede que existan diferentes opciones, debido a los campos que tiene cada tabla.
"""
def read(sock, service, msg):
    
    """
    @   Función para leer los datos de la tabla
    *   Recibe el socket, el servicio y el mensaje.
    *   Si el mensaje es 'some' se leerán los registros que cumplan con los campos del mensaje.
    """
    if msg['leer'] == 'all':
        db_sql = {
            "sql": "SELECT * FROM historial_medico WHERE rut_paciente = :rut_paciente",
            "params": {
                "rut_paciente": msg['rut_paciente']
            }
        }
        db_request=process_db_request(sock,db_sql)
        if len(db_request) == 0:
            return incode_response(service, {
                "data": "No existe historial médico."
            })
        else:
            return incode_response(service, {
                "data": db_request
            })
    
    elif msg['leer'] == 'some':
        if 'rut_paciente' in msg:
        
            db_sql = {
                "sql": "SELECT * FROM historial_medico WHERE rut_paciente = :rut_paciente",
                "params": {
                    "rut_paciente": msg['rut_paciente']
                }
            }
            db_request=process_db_request(sock,db_sql)
            if len(db_request) == 0:
                    return incode_response(service, {
                        "data": "No existe historial para la búsqueda solicitada."
                    })
            else:
                    return incode_response(service, {
                        "data": db_request
                    })
    
        elif 'rut_medico' in msg:
            db_sql = {
                "sql": "SELECT * FROM historial_medico WHERE rut_medico = :rut_medico",
                "params": {
                    "rut_medico": msg['rut_medico']
                }
            }
            db_request=process_db_request(sock,db_sql)
            if len(db_request) == 0:
                    return incode_response(service, {
                        "data": "No existe historial para la búsqueda solicitada."
                    })
            else:
                    return incode_response(service, {
                        "data": db_request
                    })
        else:
            return incode_response(service, {
                "data": "No valid options."
            })

def create(sock, service, msg):
    fields: dict = msg['crear']
    if 'descripcion' and 'rut_paciente' and "rut_medico" not in fields:
        return incode_response(service, {
            "data": "Incomplete user fields"
        })
    """
    @   Función para crear un nuevo registro en la tabla
    *   Recibe el socket, el servicio y el mensaje.
    """
    
    db_sql = {
                "sql": "INSERT INTO historial_medico (rut_paciente,rut_medico,descripcion,fecha) VALUES ("":rut_paciente,:rut_medico,:descripcion,CURRENT_TIMESTAMP)",
                "params": {
                    "rut_paciente": fields['rut_paciente'],
                    "rut_medico": fields['rut_medico'],
                    "descripcion": fields['descripcion']
                }
            }
    db_request=process_db_request(sock,db_sql)

    if 'affected_rows' in db_request:
                return incode_response(service, {
                    "data": f"Se insertaron {db_request['affected_rows']} historial(es) médico(s)."
                })
    else:
                return incode_response(service, {
                    "data": db_request
                })

def update(sock, service, msg):
    """
    @   Función para actualizar un registro en la tabla
    *   Recibe el socket, el servicio y el mensaje.
    """
    fields: dict = msg['actualizar']
    if 'descripcion' not in fields:
        return incode_response(service, {
            "data": "Incomplete user fields"
        })

    db_sql = {
            "sql": "UPDATE historial_medico SET descripcion=:descripcion WHERE id=:id",
            "params": {
            "descripcion": fields['descripcion'],
            "id": fields['id']
        }
    }
    db_request=process_db_request(sock,db_sql)
    if 'affected_rows' ==0:
        return incode_response(service, {
            "data": "No se actualizó ningún historial médico."
        })
    else:
        return incode_response(service, {
            "data": f"Se actualizó {db_request['affected_rows']} historial(es) médico(s)."
        })
          
def delete(sock, service, msg):
    """
    @   Función para borrar un registro en la tabla
    *   Recibe el socket, el servicio y el mensaje.
    """
    
    if 'borrar' in msg:
        db_sql = {
            "sql": "DELETE FROM historial_medico WHERE id=:id",
            "params": {
                "id": msg['borrar']
            }
        }
        db_request=process_db_request(sock,db_sql)
        if 'affected_rows' in db_request:
            return incode_response(service, {
                "data": f"Se eliminaron {db_request['affected_rows']} historial(es) médico(s)."
            })
        return incode_response(service, {
            "data": "Historial médico eliminado con éxito."
        })
    else:
        return incode_response(service, {
            "data": "No valid options."
        })
   
def process_request(sock, data):
    """
    @   Función para procesar los mensajes que llegan al servicio
    *   Utiliza la función decoded_data para obtener los valores importantes del mensaje.
    """
    decoded_data = decode_response(data)
    service = decoded_data['service']
    response = json.dumps(decoded_data['data'])

    if service != 'histo':
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
        elif 'borrar' in msg:
            return delete(sock=sock, service=service, msg=msg)
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

    main_service('histo', main) 
