import socket
import sys
import os
from client import input_field, service_request, print_select, print_ins_del_upd, get_session

def agendar_hora(sock, service):
    session = get_session()
    print("[ - Agendar hora - ]")
    rut_medico = input("Ingrese el rut del médico: ")
    fecha = input("Ingrese la fecha (DD-MM-AAAA): ")
    bloque_horario_id= input("Ingrese el ID del bloque: ")
    motivo = input("Ingrese el motivo de la consulta: ")
    datos = {
        "crear": {
            
            "rut_medico": rut_medico,
            "rut_paciente": session['rut'],
            "motivo": motivo,
            "fecha": fecha,
            "bloque_horario_id": bloque_horario_id
        }
    }
    status, data = service_request(sock, service, datos)
    print_ins_del_upd(status, data)
    if status == 'OK':
            print("Hora agendada con éxito.")
            sock.close()
            sys.exit()
    else:
        print(f"Error al agendar la hora: {data}.")

def ver_bloques_disponibles(sock, service):
    print("[ - Bloques disponibles - ]")
    rut_medico = input("Ingrese el rut del médico: ")
    fecha = input("Ingrese la fecha (DD-MM-AAAA): ")
    datos = {
        "leer": "some",
        "rut_medico": rut_medico,
        "fecha": fecha
    }
    status, data = service_request(sock, service, datos)
    print_select(status, data)
    if status == 'OK':
        print("Bloques disponibles mostrados con éxito.")
        sock.close()
        sys.exit()
    else:
        print(f"Error al mostrar bloques disponibles: {data}.")

def marcar_cita_atendida(sock, service):
    print("[ - Marcar cita como atendida - ]")
    cita_id = input("Ingrese el ID de la Cita: ")
    datos = {
        "actualizar": {
            "id": cita_id,
        }
    }
    status, data = service_request(sock, service, datos)
    print_ins_del_upd(status, data)
    if status == 'OK':
        print("Cita marcada como atendida con éxito.")
        sock.close()
        sys.exit()
    else:
        print(f"Error al marcar la cita como atendida: {data}.")

def print_menu_paciente():
    print("\nMenú de Agendamiento (Paciente):")
    print("1. Agendar hora")
    print("2. Ver horas disponibles")
    print("0. Salir")

def print_menu_admin():
    print("\nMenú de Agendamiento (ADMIN):")
    print("1. Agendar hora")
    print("2. Ver horas disponibles")
    print("3. Marcar cita como atendida")
    print("0. Salir")

def main_client():
    service = 'sched'
    soa_bus_host = os.getenv('SOABUS_HOST', 'soabus')
    server_address = (soa_bus_host, 5000)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect(server_address)
            session = get_session()
            
            if session['rol'] == 'admin':
                while True:
                    print("Bienvenido al sistema de agendamiento")
                    print_menu_admin()
                    choice = input("Ingrese su opcion: ")
                    if choice == '0':
                        break
                    elif choice == '1':
                        agendar_hora(sock=sock,service=service)
                    elif choice == '2':
                        ver_bloques_disponibles(sock=sock,service=service)
                    elif choice == '3':
                        marcar_cita_atendida(sock=sock,service=service)
                    else:
                        print("Opción no válida. Intente de nuevo.")
                
            elif session['rol']=='' :
                while True:
                    print("Bienvenido al sistema de agendamiento")
                    print_menu_paciente()
                    choice = input("Ingrese su opcion: ")
                    if choice == '0':
                        break
                    elif choice == '1':
                        agendar_hora(sock=sock,service=service)
                    elif choice == '2':
                        ver_bloques_disponibles(sock=sock,service=service)
                    else:
                        print("Opción no válida. Intente de nuevo.")
    
        
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