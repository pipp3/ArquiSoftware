import socket
import sys
import os
from client import input_field, service_request, print_select, print_ins_del_upd, get_session

def crear_historial_medico(sock, service):
    session=get_session()
    print("[ - Crear Historial Médico - ]")
    print("Ingrese el rut del paciente:")
    rut_paciente = input_field("Su elección: ", max_length=15)
    print("Ingrese la descripcion del historial médico:")
    descripcion = input_field("Su elección: ", max_length=200)

    datos = {
        "crear": {
            "rut_paciente": rut_paciente,
            "rut_medico": session['rut'],
            "descripcion": descripcion
        }
    }
    status, data = service_request(sock, service, datos)
    print_ins_del_upd(status, data)
    if status == 'OK':
        print("Historial médico creado con éxito.")
        sock.close()
        sys.exit()
    else:
        print(f"Error al crear el historial médico: {data}.")

def ver_historial_medico(sock, service):
    print("[ - Ver Historial Médico - ]")
    
    # Preguntar al usuario si quiere buscar por paciente o médico
    opcion = input_field("¿Desea buscar por paciente (1) o por médico (2)? (Ingrese 1 o 2): ", max_length=1)
    
    if opcion == "1":
        rut_paciente = input_field("Ingrese el rut del paciente: ", max_length=10)
        datos = {
            "leer": "some",
            "rut_paciente": rut_paciente
        }
    elif opcion == "2":
        rut_medico = input_field("Ingrese el rut del médico: ", max_length=50)
        datos = {
            "leer": "some",
            "rut_medico": rut_medico
        }
    else:
        print("Opción no válida. Inténtelo de nuevo.")
        return
    
    # Realizar la solicitud al servicio
    status, data = service_request(sock, service, datos)
    print_select(status, data)
    
    if status == 'OK':
        print("Historial médico mostrado con éxito.")
        sock.close()
        sys.exit()
    else:
        print(f"Error al mostrar el historial médico: {data}.")

def ver_historial_medico_paciente(sock, service):
    session=get_session()
    print("[ - Ver Historial Médico - ]")
    datos = {
        "leer": "all",
        "rut_paciente": session['rut']
    }
    status, data = service_request(sock, service, datos)
    print_select(status, data)
    if status == 'OK':
        print("Historial médico mostrado con éxito.")
        sock.close()
        sys.exit()
    else:
        print(f"Error al mostrar el historial médico: {data}.")

def eliminar_historial_medico(sock, service):
    print("[ - Eliminar Historial Médico - ]")
    id = input_field("Ingrese el id del historial: ", max_length=10)
    datos = {
        "borrar":id
    }
    status, data = service_request(sock, service, datos)
    print_ins_del_upd(status, data)
    if status == 'OK':
        print("Historial médico eliminado con éxito.")
        sock.close()
        sys.exit()
    else:
        print(f"Error al eliminar el historial médico: {data}.")

def actualizar_historial_medico(sock, service):
    print("[ - Actualizar Historial Médico - ]")
    id = input_field("Ingrese el id del historial: ", max_length=10)
    print("Ingrese la nueva descripción del historial médico:")
    descripcion = input_field("Su elección: ", max_length=200)
    datos = {
        "actualizar": {
            "id": id,
            "descripcion": descripcion
        }
    }
    status, data = service_request(sock, service, datos)
    print_ins_del_upd(status, data)
    if status == 'OK':
        print("Historial médico actualizado con éxito.")
        sock.close()
        sys.exit()
    else:
        print(f"Error al actualizar el historial médico: {data}.")

def print_menu_medico():
    print("\nMenú de Médico:")
    print("1. Crear historial médico")
    print("2. Ver historial médico")
    print("3. Eliminar historial médico")
    print("4. Actualizar historial médico")
    print("0. Salir")

def print_menu_paciente():
    print("\nMenú de Paciente:")
    print("1. Ver historial médico")
    print("0. Salir")
    
def main_client():
    service='histo'
    
    soa_bus_host = os.getenv('SOABUS_HOST', 'soabus')
    server_address = (soa_bus_host, 5000)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect(server_address)
            session = get_session()
            
            
            if session['rol'] == 'medico':
                while True:
                    print_menu_medico()
                    choice = input_field("Ingrese el número de la opción que desea ejecutar: ", max_length=1)
                    if choice == '0':
                        break
                    elif choice == '1':
                        crear_historial_medico(sock=sock,service= service)
                    elif choice == '2':
                        ver_historial_medico(sock=sock,service= service)
                    elif choice == '3':
                        eliminar_historial_medico(sock=sock,service= service)
                    elif choice == '4':
                        actualizar_historial_medico(sock=sock,service= service)
                    else:
                        print("Opción no válida. Intente de nuevo.")
            if session['rol']=='':
                while True:
                    print_menu_paciente()
                    choice = input_field("Ingrese el número de la opción que desea ejecutar: ", max_length=1)
                    if choice == '0':
                        break
                    elif choice == '1':
                        ver_historial_medico_paciente(sock=sock,service= service)
                    else:
                        print("Opción no válida. Intente de nuevo.")
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