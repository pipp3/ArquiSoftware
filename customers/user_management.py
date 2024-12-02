import socket
import os
from client import input_field, service_request, print_select, print_ins_del_upd


def crear_paciente(sock, service):
    print("[ - Crear Paciente - ]")
    rut = input_field("Ingrese un rut: ", max_length=20)
    nombre = input_field("Ingrese un nombre: ", max_length=20)
    apellido = input_field("Ingrese un apellido: ", max_length=20)
    celular = input_field("Ingrese un celular: ", max_length=10)
    password = input_field("Ingrese un password: ", max_length=50)
    #   Definimos la opción que elija como un diccionario
    datos = {
        "crear": {
            "rut": rut,
            "nombre": nombre,
            "apellido": apellido,
            "celular": celular,
            "password": password
        }
    }
    #   Enviamos los datos al servicio
    status, data = service_request(sock, service, datos)
    print_ins_del_upd(status, data)

def crear_funcionario(sock, service):
    print("[ - Crear Funcionario - ]")
    rut = input_field("Ingrese un rut: ", max_length=20)
    nombre = input_field("Ingrese un nombre: ", max_length=20)
    apellido = input_field("Ingrese un apellido: ", max_length=20)
    celular = input_field("Ingrese un celular: ", max_length=10)
    rol = input_field("Ingrese un rol: ", max_length=20)
    area = input_field("Ingrese un area: ", max_length=20)
    password = input_field("Ingrese un password: ", max_length=50)
    #   Definimos la opción que elija como un diccionario
    datos = {
        "crear": {
            "rut": rut,
            "nombre": nombre,
            "apellido": apellido,
            "celular": celular,
            "rol": rol,
            "area": area,
            "password": password
        }
    }
    #   Enviamos los datos al servicio
    status, data = service_request(sock, service, datos)
    print_ins_del_upd(status, data)

def leer_usuario(sock, service):
    print("[ - Leer Usuario - ]")
    print("[1] Leer todos los Pacientes.")
    print("[2] Leer todos los Funcionarios.")
    print("[3] Buscar por RUT.")
    print("[4] Buscar por Celular.")
   
    opcion = input("Ingrese una opción: ")

    if opcion == '1':
        datos = {
            "leer": "all",
            "tipo": "paciente"
        }
        status, data = service_request(sock, service, datos)
        print_select(status, data)
    elif opcion == '2':
        
        datos = {
            "leer": "all",
            "tipo": "funcionario"
        }
        status, data = service_request(sock, service, datos)
        print_select(status, data)
    elif opcion == '3':
        rut = input_field("Ingrese RUT a buscar: ", max_length=20)
        datos = {
            "leer": "some",
            "rut": rut
        }
        status, data = service_request(sock, service, datos)
        print_select(status, data)
    elif opcion == '4':
        celular = input_field("Ingrese celular a buscar: ", max_length=20)
        datos = {
            "leer": "some",
            "celular": celular
        }
        status, data = service_request(sock, service, datos)
        print_select(status, data)
    
    else:
        print("No existe esa opción.")


def actualizar_paciente(sock, service):
    print("[ - Actualizar Paciente - ]")
    print("[1] Actualizar Nombre.")
    print("[2] Actualizar Apellido.")
    print("[3] Actualizar Celular.")
    print("[4] Actualizar Password.")
    opcion = input("Ingrese una opción: ")

    rut = input_field("Ingrese Rut a actualizar: ", max_length=20)

    if opcion == '1':
        nombre = input_field("Ingrese nuevo nombre: ", max_length=20)
        datos = {
            "actualizar": {
                "tipo": "paciente",
                "rut": rut,
                "nombre": nombre
            }
        }
        status, data = service_request(sock, service, datos)
        print_ins_del_upd(status, data)
    elif opcion == '2':
        apellido = input_field("Ingrese nuevo apellido: ", max_length=20)
        datos = {
            "actualizar": {
                "tipo": "paciente",
                "rut": rut,
                "apellido": apellido
            }
        }
        status, data = service_request(sock, service, datos)
        print_ins_del_upd(status, data)
    elif opcion == '3':
        celular = input_field("Ingrese nuevo celular: ", max_length=10)
        datos = {
            "actualizar": {
                "tipo": "paciente",
                "rut": rut,
                "celular": celular
            }
        }
        status, data = service_request(sock, service, datos)
        print_ins_del_upd(status, data)
    elif opcion == '4':
        password = input_field("Ingrese nueva password: ", max_length=50)
        datos = {
            "actualizar": {
                "tipo": "paciente",
                "rut": rut,
                "password": password
            }
        }
        status, data = service_request(sock, service, datos)
        print_ins_del_upd(status, data)
    else:
        print("No existe esa opción.")

def actualizar_funcionario(sock, service):
    print("[ - Actualizar Funcionario - ]")
    print("[1] Actualizar Nombre.")
    print("[2] Actualizar Apellido.")
    print("[3] Actualizar Rol.")
    print("[4] Actualizar Area.")
    print("[5] Actualizar Celular.")
    print("[6] Actualizar Password.")
    opcion = input("Ingrese una opción: ")

    rut = input_field("Ingrese Rut a actualizar: ", max_length=20)

    if opcion == '1':
        nombre = input_field("Ingrese nuevo nombre: ", max_length=20)
        datos = {
            "actualizar": {
                "tipo": "funcionario",
                "rut": rut,
                "nombre": nombre
            }
        }
        status, data = service_request(sock, service, datos)
        print_ins_del_upd(status, data)
    elif opcion == '2':
        apellido = input_field("Ingrese nuevo apellido: ", max_length=20)
        datos = {
            "actualizar": {
                "tipo": "funcionario",
                "rut": rut,
                "apellido": apellido
            }
        }
        status, data = service_request(sock, service, datos)
        print_ins_del_upd(status, data)
    elif opcion == '3':
        rol = input_field("Ingrese nuevo rol: ", max_length=20)
        datos = {
            "actualizar": {
                "tipo": "funcionario",
                "rut": rut,
                "rol": rol
            }
        }
        status, data = service_request(sock, service, datos)
        print_ins_del_upd(status, data)
    elif opcion == '4':
        area = input_field("Ingrese nuevo area: ", max_length=10)
        datos = {
            "actualizar": {
                "tipo": "funcionario",
                "rut": rut,
                "area": area
            }
        }
        status, data = service_request(sock, service, datos)
        print_ins_del_upd(status, data)
    elif opcion == '5':
        celular = input_field("Ingrese nuevo Celular: ", max_length=50)
        datos = {
            "actualizar": {
                "tipo": "funcionario",
                "rut": rut,
                "celular": celular
            }
        }
        status, data = service_request(sock, service, datos)
        print_ins_del_upd(status, data)
    
    elif opcion == '6':
        password = input_field("Ingrese nueva password: ", max_length=50)
        datos = {
            "actualizar": {
                "tipo": "funcionario",
                "rut": rut,
                "password": password
            }
        }
        status, data = service_request(sock, service, datos)
        print_ins_del_upd(status, data)
    else:
        print("No existe esa opción.")

def borrar_usuario(sock, service):
    print("[ - Borrar Funcionario o Paciente - ]")
    rut = input_field("Ingrese un rut: ", max_length=20)
    #   Definimos la opción que elija como un diccionario
    datos = {
        "borrar": rut
    }
    #   Enviamos los datos al servicio
    status, data = service_request(sock, service, datos)
    print_ins_del_upd(status, data)


def main_client():
    """
    @   Cliente princiapl
    *   Todos los clientes deben tener esta función para ser cliente. Se conecta al bus en localhost y puerto 5000.
    *   Dentro del try se programa la lógica correspondiente al servicio.
    """
    service = 'usrmn'
    soa_bus_host=os.getenv('SOABUS_HOST', 'soabus')
    server_address = (soa_bus_host, 5000)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect(server_address)

            while True:
                print("{ -- Servicio de Manejo de Usuarios -- }")
                print("[1] Crear un Paciente.")
                print("[2] Crear un Funcionario.")
                print("[3] Leer Usuarios.")
                print("[4] Actualizar un Paciente.")
                print("[5] Actualizar un Funcionario.")
                print("[6] Borrar un Usuario.")
                print("[0] Salir.")
                opcion = input("Ingrese una opción: ")

                if opcion == '0':
                    print("Saliendo del servicio de manejo de usuarios...")
                    break

                elif opcion == '1':
                    crear_paciente(sock=sock, service=service)

                elif opcion == '2':
                    crear_funcionario(sock=sock, service=service)

                elif opcion == '3':
                    leer_usuario(sock=sock, service=service)

                elif opcion == '4':
                    actualizar_paciente(sock=sock, service=service)

                elif opcion == '5':
                    actualizar_funcionario(sock=sock, service=service)

                elif opcion == '6':
                    borrar_usuario(sock=sock, service=service)

                else:
                    print("Opción erronea. Intente nuevamente.")

        except ConnectionRefusedError:
            print(f'No se pudo conectar al bus.')

        except KeyboardInterrupt:
            print(f'Cerrando cliente {service}')

        finally:
            sock.close()


if __name__ == "__main__":
    main_client()