import json
import bcrypt   
from time import sleep
from utils.passwords import hash_password
"""
@   Manejo de usuarios
*   Este servicio recibe un JSON con las opciones que desea realizar el usuario, ya que es un CRUD.
*   'leer' para leer, 'crear' para insertar, 'borrar' para borrar, 'actualizar' para actualizar.
*   Por cada opción puede que existan diferentes opciones, debido a los campos que tiene cada tabla.
"""


def create(sock, service, msg):
    """
    @   Función para insertar un usuario en la tabla usuario
    *   Recibe un diccionario en "crear", el cual debe incluir todos los campos de usuario requeridos.
    *   Ejemplo:    "crear" : { "usuario": "hola", "nombre": "hola", "cargo": "hola" }
    """
    #   Opción de crear usuarios
    fields: dict = msg['crear']
    
    if 'rol' not in fields:

        if 'rut' and 'nombre' and 'apellido' and 'celular' and 'password' not in fields:
            return incode_response(service, {
                "data": "Incomplete user fields."
            })
    
        # Hashear la contraseña
        hashed_password = hash_password(fields['password'])
    
    
        db_sql = {
            "sql": "INSERT INTO pacientes (rut, nombre, apellido, celular, password) VALUES ("
                ":rut, :nombre, :apellido, :celular, :password)",
            "params": {
                "rut": fields['rut'],
                "nombre": fields['nombre'],
                "apellido": fields['apellido'],
                "celular": fields['celular'],
                "password": hashed_password.decode('utf-8')
            }
        }
        db_request = process_db_request(sock, db_sql)
        if 'affected_rows' in db_request:
            return incode_response(service, {
                "data": f"Se insertaron {db_request['affected_rows']} usuarios."
            })
        else:
            return incode_response(service, {
                "data": db_request
            })
    else:
        if 'rut' and 'nombre' and 'apellido' and 'rol' and 'area' and 'password' not in fields:
            return incode_response(service, {
                "data": "Incomplete user fields."
            })
        # Hashear la contraseña
        hashed_password = hash_password(fields['password'])
    
        db_sql = {
            "sql": "INSERT INTO funcionarios (rut, nombre, apellido, rol, area, password,celular) VALUES ("
                ":rut, :nombre, :apellido ,:rol, :area, :password, :celular)",
            "params": {
                "rut": fields['rut'],
                "nombre": fields['nombre'],
                "apellido": fields['apellido'],
                "rol": fields['rol'],
                "area": fields['area'],
                "password": hashed_password.decode('utf-8'),
                "celular": fields['celular']
            }
        }
        db_request = process_db_request(sock, db_sql)
        if 'affected_rows' in db_request:
            return incode_response(service, {
                "data": f"Se insertaron {db_request['affected_rows']} usuarios."
            })
        else:
            return incode_response(service, {
                "data": db_request
            })

def read(sock, service, msg):
    """
    @   Función para leer un o algunos usuarios
    *   Si el campo 'leer' es 'all', lee todos los usuarios sin filtros.
    *   Si el campo 'leer' es 'some', lee los usuarios de acuerdo su nombre de rut, nombre, cargo o area.
    *   Ejemplo:    "leer": "some", "rut": "hola"
    """
    if msg['leer'] == 'all':
        
        if msg['tipo'] == "paciente" :
            db_sql_paciente = {
                "sql": "SELECT rut, nombre, apellido ,celular FROM pacientes"
            }
            db_request = process_db_request(sock, db_sql_paciente)
            if len(db_request) == 0:
                return incode_response(service, {
                    "data": "No existen usuarios para la búsqueda solicitada."
                })
            else:
                return incode_response(service, {
                    "data": db_request
                })
        elif msg['tipo'] == 'funcionario':
            db_sql_funcionario = {
                "sql": "SELECT rut, nombre, apellido, celular, rol, area FROM funcionarios"
            }
            db_request = process_db_request(sock, db_sql_funcionario)
            if len(db_request) == 0:
                return incode_response(service, {
                    "data": "No existen usuarios para la búsqueda solicitada."
                })
            else:
                return incode_response(service, {
                    "data": db_request
                })
        else:
            return incode_response(service, {
                "data": "No valid options."
            })

    elif msg['leer'] == 'some':
        #   Opción de leer algunos usuarios, dependiendo de los campos.
        if 'rut' in msg:
            #   Leer rut según campo "rut".
            db_sql_paciente = {
                "sql": "SELECT rut,nombre,apellido,celular FROM pacientes WHERE rut = :rut",
                "params": {
                    "rut": msg['rut']
                }
            }
            db_request = process_db_request(sock, db_sql_paciente)
            if not db_request or len(db_request) == 0:
                db_sql_funcionario = {
                    "sql": "SELECT rut,nombre,apellido,celular,rol,area FROM funcionarios WHERE rut = :rut",
                    "params": {
                        "rut": msg['rut']
                    }
                }
                db_request_funcionario = process_db_request(sock, db_sql_funcionario)
                if len(db_request_funcionario) == 0:
                    return incode_response(service, {
                        "data": "No existen usuarios para la búsqueda solicitada."
                    })
                else:
                    return incode_response(service, {
                        "data": db_request_funcionario
                    })
            else:
                return incode_response(service, {
                    "data": db_request
                })
        
        elif 'celular' in msg:
            #   Leer celular según campo "celular".
            db_sql_paciente = {
                "sql": "SELECT rut,nombre,apellido,celular FROM pacientes WHERE celular = :celular",
                "params": {
                    "celular": msg['celular']
                }
            }
            db_request = process_db_request(sock, db_sql_paciente)
            if len(db_request) == 0:
                db_sql_funcionario = {
                    "sql": "SELECT rut,nombre,apellido,celular,rol,area FROM funcionarios WHERE celular = :celular",
                    "params": {
                        "celular": msg['celular']
                    }
                }
                db_request_funcionario = process_db_request(sock, db_sql_funcionario)
                if len(db_request_funcionario) == 0:
                    return incode_response(service, {
                        "data": "No existen usuarios para la búsqueda solicitada."
                    })
                else:
                    return incode_response(service, {
                        "data": db_request_funcionario
                    })
            else:
                return incode_response(service, {
                    "data": db_request
                })
        
        else:
            #   No se incluyeron campos de lectura.
            return incode_response(service, {
                "data": "Query SQL Incompleta. Por favor revisar los campos solicitados."
            })


def update(sock, service, msg):
    """
    @   Función para actualizar un usuario.
    *   Recibe un diccionario en la llave 'update' de msg, que debe incluir el usuario a actualizar y el campo.
    *   Los campos que se pueden actualizar son nombre, cargo, area o password.
    *   Ejemplo:    "actualizar": { "usuario": "hola", "password": "123" }
    """
    #   Opción de actualizar usuarios
    fields: dict = msg['actualizar']
    
    if fields['tipo'] == 'paciente':
        if 'rut' not in fields:
            return incode_response(service, {
                "data": "Incomplete user fields."
            })
        else:
            if 'nombre' in fields:
                db_sql = {
                    "sql": "UPDATE pacientes SET nombre = :nombre WHERE rut = :rut",
                    "params": {
                        "nombre": fields['nombre'],
                        "rut": fields['rut']
                    }
                }
                db_request = process_db_request(sock, db_sql)
                if 'affected_rows' in db_request:
                    return incode_response(service, {
                        "data": f"Se actualizaron {db_request['affected_rows']} usuarios."
                    })
                else:
                    return incode_response(service, {
                        "data": db_request
                    })
            elif 'apellido' in fields:
                db_sql = {
                    "sql": "UPDATE pacientes SET apellido = :apellido WHERE rut = :rut",
                    "params": {
                        "apellido": fields['apellido'],
                        "rut": fields['rut']
                    }
                }
                db_request = process_db_request(sock, db_sql)
                if 'affected_rows' in db_request:
                    return incode_response(service, {
                        "data": f"Se actualizaron {db_request['affected_rows']} usuarios."
                    })
                else:
                    return incode_response(service, {
                        "data": db_request
                    })
            elif 'celular' in fields:
                
                db_sql = {
                    "sql": "UPDATE pacientes SET celular = :celular WHERE rut = :rut",
                    "params": {
                        "celular": fields['celular'],
                        "rut": fields['rut']
                    }
                }
                db_request = process_db_request(sock, db_sql)
                if 'affected_rows' in db_request:
                    return incode_response(service, {
                        "data": f"Se actualizaron {db_request['affected_rows']} usuarios."
                    })
                else:
                    return incode_response(service, {
                        "data": db_request
                    })
            elif 'password' in fields:
                # Hashear la contraseña
                hashed_password = hash_password(fields['password'])
                db_sql = {
                    "sql": "UPDATE pacientes SET password = :password WHERE rut = :rut",
                    "params": {
                        "password": hashed_password.decode('utf-8'),
                        "rut": fields['rut']
                    }
                }
                db_request = process_db_request(sock, db_sql)
                if 'affected_rows' in db_request:
                    return incode_response(service, {
                        "data": f"Se actualizaron {db_request['affected_rows']} usuarios."
                    })
                else:
                    return incode_response(service, {
                        "data": db_request
                    })
            else:
                return incode_response(service, {
                    "data": "No valid options. aqui 1"
                })
    elif fields["tipo"] == 'funcionario':
        if 'rut' not in fields:
            return incode_response(service, {
                "data": "Incomplete user fields."
            })
        else:
            if 'nombre' in fields:
                db_sql = {
                    "sql": "UPDATE funcionarios SET nombre = :nombre WHERE rut = :rut",
                    "params": {
                        "nombre": fields['nombre'],
                        "rut": fields['rut']
                    }
                }
                db_request = process_db_request(sock, db_sql)
                if 'affected_rows' in db_request:
                    return incode_response(service, {
                        "data": f"Se actualizaron {db_request['affected_rows']} usuarios."
                    })
                else:
                    return incode_response(service, {
                        "data": db_request
                    })
            elif 'apellido' in fields:
                db_sql = {
                    "sql": "UPDATE funcionarios SET apellido = :apellido WHERE rut = :rut",
                    "params": {
                        "apellido": fields['apellido'],
                        "rut": fields['rut']
                    }
                }
                db_request = process_db_request(sock, db_sql)
                if 'affected_rows' in db_request:
                    return incode_response(service, {
                        "data": f"Se actualizaron {db_request['affected_rows']} usuarios."
                    })
                else:
                    return incode_response(service, {
                        "data": db_request
                    })
            elif 'rol' in fields:
                db_sql = {
                    "sql": "UPDATE funcionarios SET rol = :rol WHERE rut = :rut",
                    "params": {
                        "rol": fields['rol'],
                        "rut": fields['rut']
                    }
                }
                db_request = process_db_request(sock, db_sql)
                if 'affected_rows' in db_request:
                    return incode_response(service, {
                        "data": f"Se actualizaron {db_request['affected_rows']} usuarios."
                    })
                else:
                    return incode_response(service, {
                        "data": db_request
                    })
            elif 'area' in fields:
                db_sql = {
                    "sql": "UPDATE funcionarios SET area = :area WHERE rut = :rut",
                    "params": {
                        "area": fields['area'],
                        "rut": fields['rut']
                    }
                }
                db_request = process_db_request(sock, db_sql)
                if 'affected_rows' in db_request:
                    return incode_response(service, {
                        "data": f"Se actualizaron {db_request['affected_rows']} usuarios."
                    })
                else:
                    return incode_response(service, {
                        "data": db_request
                    })
            elif 'password' in fields:
                # Hashear la contraseña
                hashed_password = hash_password(fields['password'])
                db_sql = {
                    "sql": "UPDATE funcionarios SET password = :password WHERE rut = :rut",
                    "params": {
                        "password": hashed_password.decode('utf-8'),
                        "rut": fields['rut']
                    }
                }
                db_request = process_db_request(sock, db_sql)
                if 'affected_rows' in db_request:
                    return incode_response(service, {
                        "data": f"Se actualizaron {db_request['affected_rows']} usuarios."
                    })
                else:
                    return incode_response(service, {
                        "data": db_request
                    })
    else:
        return incode_response(service, {
        "data": "No valid options. aqui2"
        })
       


def delete(sock, service, msg):
    """
    @   Función para borrar un usuario de acuerdo a su nombre de usuario.
    *   Ejemplo:    "borrar": "juanito"
    """
    #   Opción de borrar usuarios
        
    db_sql_paciente = {
            "sql": "DELETE FROM pacientes WHERE rut = :rut",
            "params": {
                "rut": msg['borrar']
            }
        }
    db_request = process_db_request(sock, db_sql_paciente)
    if 'affected_rows' in db_request:
            return incode_response(service, {
                "data": f"Se elimino {db_request['affected_rows']} usuarios."
            })
    else:
        db_sql_funcionario = {
                "sql": "DELETE FROM funcionarios WHERE rut = :rut",
                "params": {
                    "rut": msg['borrar']
                }
            }
        db_request_funcionario = process_db_request(sock, db_sql_funcionario)
        if 'affected_rows' in db_request_funcionario:
                return incode_response(service, {
                    "data": f"Se elimino {db_request_funcionario['affected_rows']} usuarios."
                })
        else:
                return incode_response(service, {
                    "data": db_request_funcionario
                })
        



def process_request(sock, data):
    """
    @   Función para procesar los mensajes que llegan al servicio
    *   Utiliza la función decoded_data para obtener los valores importantes del mensaje.
    """
    decoded_data = decode_response(data)
    service = decoded_data['service']
    response = json.dumps(decoded_data['data'])

    if service != 'usrmn':
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
                "data": "No valid options.aqui3"
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

    main_service('usrmn', main)  # Use "usrmn" as the service