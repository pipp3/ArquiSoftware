import json
from time import sleep

def create(sock, service, msg):
    """
    @   Función create
    *   Función para crear una receta.
    """
    fields: dict = msg['crear']

    # Verificar que todos los campos necesarios estén presentes
    if 'cita_id' not in fields or 'medicamento' not in fields or 'dosis' not in fields or 'frecuencia' not in fields or 'duracion' not in fields:
        return incode_response(service, {
            "data": "Incomplete user fields"
        })

    # Realizar la creación de la receta en la base de datos
    db_sql = {
        "sql": """
            INSERT INTO recetas (cita_id, medicamento, dosis, frecuencia, duracion)
            VALUES (:cita_id, :medicamento, :dosis, :frecuencia, :duracion)
        """,
        "params": {
            "cita_id": fields['cita_id'],
            "medicamento": fields['medicamento'],
            "dosis": fields['dosis'],
            "frecuencia": fields['frecuencia'],
            "duracion": fields['duracion']
        }
    }
    db_request = process_db_request(sock, db_sql)
    if len(db_request) == 0:
        return incode_response(service, {
            "data": "Error creating recipe"
        })
    else:
        return incode_response(service, {
            "data": "Recipe created successfully"
        })
def read(sock, service, msg):
    """
    @   Función read
    *   Función para leer una receta.
    """
    

    # Realizar la lectura de la receta en la base de datos
    if 'id' in msg:
        db_sql = {
            "sql": """
                SELECT * FROM recetas
                WHERE id = :id
            """,
            "params": {
                "id": msg['id']
            }
        }
        db_request = process_db_request(sock, db_sql)
        if len(db_request) == 0:
            return incode_response(service, {
                "data": "Recipe not found"
            })
        else:
            return incode_response(service, {
                "data": db_request
            })
    elif msg['leer'] == 'some' and 'cita_id' in msg and 'rut_paciente' in msg:
        db_sql = {
            "sql": """
                SELECT r.*
                FROM recetas r
                INNER JOIN citas c ON r.cita_id = c.id
                WHERE c.rut_paciente = :rut_paciente AND r.cita_id = :cita_id
            """,
            "params": {
                "rut_paciente": msg['rut_paciente'],
                "cita_id": msg['cita_id']
            }
        }
        db_request = process_db_request(sock, db_sql)
        if len(db_request) == 0:
            return incode_response(service, {
                "data": "No recipes found"
            })
        else:
            return incode_response(service, {
                "data": db_request
            })
    elif msg['leer'] == 'some' and 'rut_paciente' in msg:
        db_sql = {
            "sql": """
                SELECT r.*
                FROM recetas r
                INNER JOIN citas c ON r.cita_id = c.id
                WHERE c.rut_paciente = :rut_paciente
                ORDER BY r.id DESC
                LIMIT 10
            """,
            "params": {
                "rut_paciente": msg['rut_paciente']
            }
        }
        db_request = process_db_request(sock, db_sql)
        if len(db_request) == 0:
            return incode_response(service, {
                "data": "No recipes found"
            })
        else:
            return incode_response(service, {
                "data": db_request
            })
    else:
        return incode_response(service, {
            "data": "Incomplete user fields"
        })
    
def delete(sock, service, msg):
    """
    @   Función delete
    *   Función para eliminar una receta.
    """

    # Realizar la eliminación de la receta en la base de datos
    
    db_sql = {
        "sql": """
            DELETE FROM recetas
            WHERE id = :id
        """,
        "params": {
            "id": msg['eliminar']
        }
    }
    db_request = process_db_request(sock, db_sql)
    if len(db_request) == 0:
        return incode_response(service, {
            "data": "Recipe not found"
        })
    else:
        return incode_response(service, {
            "data": "Recipe deleted successfully"
        })
    


def process_request(sock, data):
    """
    @   Función para procesar los mensajes que llegan al servicio
    *   Utiliza la función decoded_data para obtener los valores importantes del mensaje.
    """
    decoded_data = decode_response(data)
    service = decoded_data['service']
    response = json.dumps(decoded_data['data'])

    if service != 'recip':
        return incode_response(service, {
            "data": "Invalid Service: " + service
        })

    try:
        msg = json.loads(response)
        if 'leer' in msg:
            return read(sock=sock, service=service, msg=msg)
       
        elif 'crear' in msg:
            return create(sock=sock, service=service, msg=msg)
        elif 'eliminar' in msg:
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

    main_service('recip', main)  # Use "usrmn" as the service