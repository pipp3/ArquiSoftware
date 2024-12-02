import socket
import sys
import os
from client import input_field, service_request, print_select, print_ins_del_upd, get_session

def cancelar_hora(sock, service):
    session = get_session()
    print("[ - Cancelar Hora - ]")
    cita_id = input_field("Ingrese el ID de la cita a cancelar: ", max_length=10)
    datos = {
        "cancelar": {
            "cita_id": cita_id,
        }
    }
    status, data = service_request(sock, service, datos)
    print_ins_del_upd(status, data)
    if status == 'OK':
        print("Hora cancelada con éxito.")
        sock.close()
        sys.exit()
    else:
        print(f"Error al cancelar la hora: {data}.")

def leer_horas_canceladas(sock, service):
    print("[ - Leer Horas Canceladas - ]")
    print("1. Leer las ultimas horas canceladas.")
    print("2. Leer horas canceladas por paciente.")
    print("3. Leer horas canceladas por médico.")
    print("0. Salir")
    choice = input_field("Ingrese el número de la opción que desea ejecutar: ", max_length=1)
    if choice == '0':
        return
    elif choice == '1':
        datos = {
            "leer":"all"
        }
        status, data = service_request(sock, service, datos)
        print_select(status, data)
    elif choice == '2':
        rut_paciente = input_field("Ingrese el rut del paciente: ", max_length=20)
        datos = {
            "leer":"some",
            "rut_paciente": rut_paciente
        }
        status, data = service_request(sock, service, datos)
        print_select(status, data)
    elif choice == '3':
        rut_medico = input_field("Ingrese el rut del médico: ", max_length=20)
        datos = {
            "leer":"some",
            "rut_medico": rut_medico
        }
        status, data = service_request(sock, service, datos)
        print_select(status, data)


def print_menu_admin():
    print("\n[ - Servicio de Cancelación de Horas (Admin) - ]")
    print("[1] Cancelar Hora.")
    print("[2] Leer Horas Canceladas.")
    print("[0] Salir")

def print_menu_paciente():
    print("\n[ - Servicio de Cancelación de Horas (Paciente) - ]")
    print("[1] Cancelar Hora.")
    print("[0] Salir")

def main_client():
    service = 'cance'
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
                        cancelar_hora(sock=sock,service= service)
                    elif choice == '2':
                        leer_horas_canceladas(sock=sock, service= service)
                    else:
                        print("Opción no válida. Intente de nuevo.")
                        
            elif session['rol']=='':
                while True:
                    print_menu_paciente()
                    choice = input_field("Ingrese el número de la opción que desea ejecutar: ", max_length=1)
                    if choice == '0':
                        break
                    elif choice == '1':
                        cancelar_hora(sock=sock,service= service)
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