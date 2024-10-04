import socket


def main_client():
    """
    @   Cliente princiapl
    *   Todos los clientes deben tener esta función para ser cliente. Se conecta al bus en localhost y puerto 5000.
    *   Dentro del try se programa la lógica correspondiente al servicio.
    """
    service = 'dbcon'
    server_address = ('localhost', 5000)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect(server_address)
            datos = {
                "sql": "SELECT usuario FROM usuario WHERE nombre = :nombre",
                "params": {
                    "nombre": "Nico"
                }
            }
            send_message(sock, service, datos)
            respuesta = receive_response(sock)
            print("Respuesta: ", respuesta)
        except ConnectionRefusedError:
            print(f'No se pudo conectar al bus.')
        except KeyboardInterrupt:
            print(f'Cerrando cliente {service}')
        finally:
            sock.close()


if __name__ == "__main__":
    from client import send_message, receive_response

    main_client()