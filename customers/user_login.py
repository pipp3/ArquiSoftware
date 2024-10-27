import socket
import json
import sys
import os 

def main_client():
    """
    @   Cliente princiapl
    *   Todos los clientes deben tener esta función para ser cliente. Se conecta al bus en localhost y puerto 5000.
    *   Dentro del try se programa la lógica correspondiente al servicio.
    """
    service = 'usrlg'
    soa_bus_host=os.getenv('SOABUS_HOST', 'soabus')
    server_address = (soa_bus_host, 5000)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect(server_address)

            while True:
                usuario = input_field("Ingrese un usuario: ", max_length=20)
                password = input_field("Ingrese su contraseña: ", max_length=50)
                #   Definimos la opción que elija como un diccionario
                datos = {
                    "login": {
                        "usuario": usuario,
                        "password": password
                    }
                }
                #   Enviamos los datos al servicio
                status, data = service_request(sock, service, datos)
                if status == 'OK':
                    autenticacion = data['autenticado']
                    if autenticacion == 'true':
                        save_session(data)
                        print(f"Inicio de sesión exitoso. Se iniciará el servicio.")
                        sock.close()
                        sys.exit()
                    else:
                        save_session(data)
                        print("Credenciales inválidas, intente nuevamente.")
                else:
                    print(f"Ocurrió un error: {data}")

        except ConnectionRefusedError:
            print(f'No se pudo conectar al bus.')

        except KeyboardInterrupt:
            print(f'Cerrando cliente {service}')

        finally:
            sock.close()


if __name__ == "__main__":
    from client import input_field, service_request, save_session

    main_client()