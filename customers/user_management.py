import socket
import os
from client import input_field, service_request, print_select, print_ins_del_upd


def crear_usuario(sock, service):
    print("[ - Crear Usuario - ]")
    usuario = input_field("Ingrese un usuario: ", max_length=20)
    nombre = input_field("Ingrese un nombre: ", max_length=20)
    cargo = input_field("Ingrese un cargo: ", max_length=20)
    area = input_field("Ingrese un area: ", max_length=10)
    password = input_field("Ingrese un password: ", max_length=50)
    #   Definimos la opción que elija como un diccionario
    datos = {
        "crear": {
            "usuario": usuario,
            "nombre": nombre,
            "cargo": cargo,
            "area": area,
            "password": password
        }
    }
    #   Enviamos los datos al servicio
    status, data = service_request(sock, service, datos)
    print_ins_del_upd(status, data)


def leer_usuario(sock, service):
    print("[ - Leer Usuario - ]")
    print("[1] Leer todos los usuarios.")
    print("[2] Buscar por Usuario.")
    print("[3] Buscar por Nombre.")
    print("[4] Buscar por Cargo.")
    print("[5] Buscar por Tipo.")
    opcion = input()

    if opcion == '1':
        datos = {
            "leer": "all"
        }
        status, data = service_request(sock, service, datos)
        print_select(status, data)
    elif opcion == '2':
        usuario = input_field("Ingrese usuario a buscar: ", max_length=20)
        datos = {
            "leer": "some",
            "usuario": usuario
        }
        status, data = service_request(sock, service, datos)
        print_select(status, data)
    elif opcion == '3':
        nombre = input_field("Ingrese nombre a buscar: ", max_length=20)
        datos = {
            "leer": "some",
            "nombre": nombre
        }
        status, data = service_request(sock, service, datos)
        print_select(status, data)
    elif opcion == '4':
        cargo = input_field("Ingrese cargo a buscar: ", max_length=20)
        datos = {
            "leer": "some",
            "cargo": cargo
        }
        status, data = service_request(sock, service, datos)
        print_select(status, data)
    elif opcion == '5':
        area = input_field("Ingrese area a buscar: ", max_length=10)
        datos = {
            "leer": "some",
            "area": area
        }
        status, data = service_request(sock, service, datos)
        print_select(status, data)
    else:
        print("No existe esa opción.")


def actualizar_usuario(sock, service):
    print("[ - Actualizar Usuario - ]")
    print("[1] Actualizar Nombre.")
    print("[2] Actualizar Cargo.")
    print("[3] Actualizar Tipo.")
    print("[4] Actualizar Password.")
    opcion = input()

    usuario = input_field("Ingrese usuario a actualizar: ", max_length=20)

    if opcion == '1':
        nombre = input_field("Ingrese nuevo nombre: ", max_length=20)
        datos = {
            "actualizar": {
                "usuario": usuario,
                "nombre": nombre
            }
        }
        status, data = service_request(sock, service, datos)
        print_ins_del_upd(status, data)
    elif opcion == '2':
        cargo = input_field("Ingrese nuevo cargo: ", max_length=20)
        datos = {
            "actualizar": {
                "usuario": usuario,
                "cargo": cargo
            }
        }
        status, data = service_request(sock, service, datos)
        print_ins_del_upd(status, data)
    elif opcion == '3':
        area = input_field("Ingrese nuevo area: ", max_length=10)
        datos = {
            "actualizar": {
                "usuario": usuario,
                "area": area
            }
        }
        status, data = service_request(sock, service, datos)
        print_ins_del_upd(status, data)
    elif opcion == '4':
        password = input_field("Ingrese nueva password: ", max_length=50)
        datos = {
            "actualizar": {
                "usuario": usuario,
                "password": password
            }
        }
        status, data = service_request(sock, service, datos)
        print_ins_del_upd(status, data)
    else:
        print("No existe esa opción.")


def borrar_usuario(sock, service):
    print("[ - Borrar Usuario - ]")
    usuario = input_field("Ingrese un usuario: ", max_length=20)
    #   Definimos la opción que elija como un diccionario
    datos = {
        "borrar": usuario
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
                print("[1] Crear un Usuario.")
                print("[2] Leer Usuarios.")
                print("[3] Actualizar un Usuario.")
                print("[4] Borrar un Usuario.")
                print("[0] Salir.")
                opcion = input()

                if opcion == '0':
                    print("Saliendo del servicio de manejo de usuarios...")
                    break

                elif opcion == '1':
                    crear_usuario(sock=sock, service=service)

                elif opcion == '2':
                    leer_usuario(sock=sock, service=service)

                elif opcion == '3':
                    actualizar_usuario(sock=sock, service=service)

                elif opcion == '4':
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