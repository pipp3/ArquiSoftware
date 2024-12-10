import socket
import sys
import os
from client import input_field, service_request, print_select, print_ins_del_upd, get_session

def crear_notificacion(sock, service):
    print("[ - Crear Notificación - ]")
    cita_id = input("Ingrese el ID de la cita: ")
    mensaje = input("Ingrese el mensaje de la notificación: ")
    destino = input("Ingrese el celular destino de la notificación: ")

    datos = {
        "crear": {
            "cita_id": cita_id,
            "mensaje": mensaje,
            "destino": destino
        }
    }
    status, data = service_request(sock, service, datos)
    print_ins_del_upd(status, data)
    if status == 'OK':
        print("Notificación creada con éxito.")
        sock.close()
        sys.exit()
    else:
        print(f"Error al crear la notificación: {data}.")

def leer_notificacion(sock, service):
    print("[ - Leer Notificación - ]")
    print("[1] Leer las ultimas 5 notificaciones creadas.")
    print("[2] Buscar por ID de la notificacion.")
    print("[3] Filtrar las ultimas 5 notificaciones por paciente.")
    print("[4] Buscar notificaciones por ID de la cita.")
    print("[5] Filtrar las ultimas 5 notifiaciones por medico.")
    print("[0] Salir.")
    opcion = input_field("Su elección: ", max_length=1)

    if opcion == '1':
        datos = {
            "leer": "all"
        }
    elif opcion == '2':
        id = input_field("Ingrese el ID a buscar: ", max_length=10)
        datos = {
            "leer": "some",
            "id": id
        }
    elif opcion == '3':
        rut_paciente = input_field("Ingrese RUT del paciente: ", max_length=10)
        datos = {
            "leer": "some",
            "rut_paciente": rut_paciente
        }
    elif opcion == '4':
        cita_id = input_field("Ingrese el ID de la cita: ", max_length=10)
        datos = {
            "leer": "some",
            "cita_id": cita_id
        }
    elif opcion == '5':
        rut_medico = input_field("Ingrese RUT del médico: ", max_length=10)
        datos = {
            "leer": "some",
            "rut_medico": rut_medico
        }   
    elif opcion == '0':
        print("Saliendo del menú de notificaciones.")
        sock.close()
        sys.exit()
    else:
        print("Opción no válida.")
        return

    status, data = service_request(sock, service, datos)
    print_select(status, data)
    if status == 'OK':
        print("Notificación mostrada con éxito.")
        sock.close()
        sys.exit()
    else:
        print(f"Error al mostrar la notificación: {data}.")

def leer_notificacion_paciente(sock, service):
    session = get_session()

    while True:
        print("[ - Leer Notificación - ]")
        print("[1] Leer tus últimas 5 notificaciones.")
        print("[2] Buscar por ID.")
        print("[0] Salir.")

        opcion = input_field("Su elección: ", max_length=1)

        # Salir
        if opcion == '0':
            print("Saliendo del menú de notificaciones.")
            break

        # Leer las últimas 5 notificaciones
        elif opcion == '1':
            datos = {
                "leer": "some",
                "rut": session['rut']
            }
            status, data = service_request(sock, service, datos)
            print_select(status, data)
        
        # Buscar por ID
        elif opcion == '2':
            id = input_field("Ingrese el ID a buscar: ", max_length=10)
            datos = {
                "leer": "some",
                "id_noti": id,
                "rut": session['rut']
            }
            status, data = service_request(sock, service, datos)
            print_select(status, data)
        
        
        else:
            print("Opción no válida.")
            return



def print_menu_admin():
    print("\nServicio de notificaciones:")
    print("[1] Crear notificación.")
    print("[2] Leer notificación.")
    print("[0] Salir.")
    

def main_client():
    service = 'notif'
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
                        crear_notificacion(sock=sock,service= service)
                    elif choice == '2':
                        leer_notificacion(sock=sock,service= service)
                    else:
                        print("Opción no válida. Intente de nuevo.")
            elif session['rol']=='' or session['rol']=='medico':
                    leer_notificacion_paciente(sock, service)
                        
            else:
                print(f"Error: Rol no reconocido: {session['rol']}")

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