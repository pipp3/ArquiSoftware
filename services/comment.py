import json
from time import sleep

"""
@   Manejo de comentarios
*   Este servicio recibe un JSON con las opciones que desea realizar el usuario, ya que es un CRUD.
*   'leer' para leer, 'crear' para insertar, 'borrar' para borrar, 'actualizar' para actualizar.
*   Por cada opción puede que existan diferentes opciones, debido a los campos que tiene cada tabla.
"""

def create(sock, service,msg):
    fields: dict = msg['crear']

    if 'comentario' and 'paciente_id' and 'tipo' and 'calificacion' not in fields:
        return incode_response(service,{
            "data":"Incomplete user fields"
        })
    db_sql = {
        "sql":"INSERT INTO comentario (paciente_id,comentario,tipo,calificacion,fecha) VALUES ("":paciente_id,:comentario,:tipo,:calificacion,CURRENT_TIMESTAMP)",
        "params":{
            "paciente_id":fields['paciente_id'],
            "comentario":fields['comentario'],
            "tipo":fields['tipo'],
            "calificacion":fields['calificacion']
        },
    }
    db_request=process_db_request(sock,db_sql)
    if 'affected_rows' in db_request:
        return incode_response(service,{
            "data": f"Se insertaron {db_request['affected_rows']} comentario(s)."
        })
    else:
        return incode_response(service,{
            "data": db_request
        })
    
def read(sock, service, msg):
    if msg["leer"]=="all":
        db_sql={
            "sql":"SELECT * FROM comentario ORDER BY id DESC LIMIT 5",
            "params":{}
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
    elif msg["leer"]=="some":
        if "id_comment" in msg:
            db_sql={
                "sql":"SELECT * FROM comentario WHERE id=:id_comment",
                "params":{
                    "id_comment":msg["id_comment"]
                }
            }
            db_request=process_db_request(sock,db_sql)
            if(len(db_request)==0):
                return incode_response(service,{
                    "data":"No comment found."
                })
            else:
                return incode_response(service,{
                    "data":db_request
                })
        elif "paciente_id" in msg:
            db_sql={
                "sql":"SELECT * FROM comentario WHERE paciente_id=:paciente_id ORDER BY id DESC LIMIT 5",
                "params":{
                    "paciente_id":msg["paciente_id"]
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
        elif "tipo" in msg:
            db_sql={
                "sql":"SELECT * FROM comentario WHERE tipo=:tipo ORDER BY id DESC LIMIT 5",
                "params":{
                    "tipo":msg["tipo"]
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

def process_request(sock, data):
    """
    @   Función para procesar los mensajes que llegan al servicio
    *   Utiliza la función decoded_data para obtener los valores importantes del mensaje.
    """
    decoded_data = decode_response(data)
    service = decoded_data['service']
    response = json.dumps(decoded_data['data'])

    if service != 'comme':
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

    main_service('comme', main)  # Use "usrmn" as the service