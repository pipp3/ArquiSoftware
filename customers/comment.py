import socket
import sys
import os
from client import input_field, service_request, print_select, print_ins_del_upd, get_session

def crear_comentario(sock, service):
    session = get_session()
    print("[ - Crear Comentario - ]")
    print("Ingrese el tipo de comentario:")
    print("[1] Queja.")
    print("[2] Sugerencia.")
    print("[3] Felicitación.")
    tipo = input_field("Su elección: ", max_length=1)
    if tipo == '1':
        tipo = "queja"
    elif tipo == '2':
        tipo = "sugerencia"
    elif tipo == '3':
        tipo = "felicitacion"
    else:
        print("Opción no válida")
        return

    contenido = input("Ingrese su comentario: ")
    calificacion = input_field("Ingrese una calificación (1 al 5): ", max_length=1)
    
    datos = {
        "crear": {
            "contenido": contenido,
            "rut_paciente": session['rut'],
            "tipo": tipo,
            "calificacion": calificacion
        }
    }
    status, data = service_request(sock, service, datos)
    print_ins_del_upd(status, data)
    if status == 'OK':
        print("Comentario creado con éxito.")
        sock.close()
        sys.exit()
    else:
        print(f"Error al crear el comentario: {data}.")
    


def leer_comentario(sock, service):
    print("[ - Leer Comentario - ]")
    print("[1] Leer los ultimos 5 comentarios.")
    print("[2] Buscar por Comentario.")
    print("[3] Filtrar los ultimos 5 comentarios por usuario.")
    print("[4] Filtrar los ultimos 5 comentarios por tipo.")
    opcion = input_field("Su elección: ", max_length=1)

    if opcion == '1':
        datos = {
            "leer": "all"
        }
    elif opcion == '2':
        id_comment = input_field("Ingrese ID del comentario a buscar: ", max_length=10)
        datos = {
            "leer": "some",
            "id": id_comment
        }
    elif opcion == '3':
        rut_paciente = input_field("Ingrese RUT del usuario a buscar: ", max_length=20)
        datos = {
            "leer": "some",
            "rut_paciente": rut_paciente
        }
    elif opcion == '4':
        tipo = input_field("Ingrese tipo a buscar: ", max_length=20)
        datos = {
            "leer": "some",
            "tipo": tipo
        }
    else:
        print("Opción no válida")
        return

    status, data = service_request(sock, service, datos)
    print_select(status, data)

def print_menu_admin():
    print("\n[ - Servicio de Comentarios (Admin) - ]")
    print("[1] Leer Comentarios.")
    print("[0] Salir.")

def print_menu_paciente():
    print("\n[ - Servicio de Comentarios (Paciente) - ]")
    print("[1] Crear Comentario.")
    print("[0] Salir.")

def main_client():
    service = 'comme'
    soa_bus_host = os.getenv('SOABUS_HOST', 'soabus')
    server_address = (soa_bus_host, 5000)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect(server_address)
            session = get_session()
                
            if session['rol'] == 'admin':
                while True:
                    print_menu_admin()
                    choice = input_field("Ingrese el número de la opción que desea ejecutar: ", max_length=1)
                    if choice == '0':
                        break
                    elif choice == '1':
                        leer_comentario(sock=sock,service= service)
                    else:
                        print("Opción no válida. Intente de nuevo.")
                        
            elif session['rol']=='':
                while True:
                    print_menu_paciente()
                    choice = input_field("Ingrese el número de la opción que desea ejecutar: ", max_length=1)
                    if choice == '0':
                        break
                    elif choice == '1':
                        crear_comentario(sock=sock,service= service)
                    else:
                        print("Opción no válida. Intente de nuevo.")
            else:
                print(f"Error: Cargo no reconocido: {session['cargo']}")

        except ConnectionRefusedError:
            print('No se pudo conectar al bus.')
        except KeyboardInterrupt:
            print(f'Cerrando cliente {service}')
        except Exception as e:
            print(f"Error inesperado: {str(e)}")
        finally:
            sock.close()

if __name__ == "__main__":
    main_client()