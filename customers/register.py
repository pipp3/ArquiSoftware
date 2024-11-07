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
                
                print("[0] Salir.")
                opcion = input()

                if opcion == '0':
                    print("Saliendo del servicio de manejo de usuarios...")
                    break

                elif opcion == '1':
                    crear_usuario(sock=sock, service=service)

               

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