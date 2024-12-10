import socket
import sys
import os
from client import input_field, service_request, print_select, print_ins_del_upd, get_session

def actualizar_hora(sock, service):
    session = get_session()
    print("[ - Re-Agendar Hora - ]")
    cita_id = input_field("Ingrese el ID de la cita a re-agendar: ", max_length=10)
    fecha = input("Ingrese la nueva fecha de la cita (DD-MM-AAAA): ")
    datos = {
        "actualizar":"some",
        "cita_id": cita_id,
        "fecha": fecha,
        
    }
    status, data = service_request(sock, service, datos)
    print_ins_del_upd(status, data)
    if status == 'OK':
        print("Hora re-agendada con éxito.")
        sock.close()
        sys.exit()
    else:
        print(f"Error al re-agendar la hora: {data}.")

def listar_citas(sock, service):
    session = get_session()
    print("[ - Listar Citas de un paciente - ]")
    rut_paciente = input_field("Ingrese el RUT del paciente: ", max_length=20)
    datos = {
        "leer":"some",
        "rut_paciente": rut_paciente
        
    }
    status, data = service_request(sock, service, datos)
    print_select(status, data)
    if status == 'OK':
        print("Citas mostradas con éxito.")
        sock.close()
        sys.exit()
    else:
        print(f"Error al mostrar las citas: {data}.")

def listar_mis_citas(sock, service):
    session = get_session()
    print("[ - Listar Mis Citas - ]")
    datos = {
        "leer":"some",
        "rut_paciente": session['rut']
        
    }
    status, data = service_request(sock, service, datos)
    print_select(status, data)
    if status == 'OK':
        print("Citas mostradas con éxito.")
        sock.close()
        sys.exit()
    else:
        print(f"Error al mostrar las citas: {data}.")

def print_menu_admin():
    print("\n[ - Servicio de Re-Agendacion de Horas (Admin) - ]")
    print("[1] Re-Agendar Hora.")
    print("[2] Listar Citas de un paciente.")
    print("[0] Salir.")

def print_menu_paciente():
    print("\n[ - Servicio de Re-Agendacionn de Horas (Paciente) - ]")
    print("[1] Re-Agendar Hora.")
    print("[2] Listar Mis Citas.")
    print("[0] Salir.")

def main_client():
    service = 'resch'
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
                        actualizar_hora(sock=sock,service= service)
                    elif choice == '2':
                        listar_citas(sock=sock,service= service)
                    else:
                        print("Opción no válida. Intente de nuevo.")
                        
            elif session['rol']=='':
                while True:
                    print_menu_paciente()
                    choice = input_field("Ingrese el número de la opción que desea ejecutar: ", max_length=1)
                    if choice == '0':
                        break
                    elif choice == '1':
                        actualizar_hora(sock=sock,service= service)
                    elif choice == '2':
                        listar_mis_citas(sock=sock,service= service)
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