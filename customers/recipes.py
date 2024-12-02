import socket
import sys
import os
from client import input_field, service_request, print_select, print_ins_del_upd, get_session

def crear_receta(sock,service):
    print("\n[ - Crear Receta - ]")
    cita_id = input("Ingrese el id de la cita: ")
    medicamento = input("Ingrese el medicamento: ")
    dosis = input("Ingrese la dosis: ")
    frecuencia = input("Ingrese la frecuencia: ")
    duracion = input("Ingrese la duracion: ")
    datos = {
        "crear":
        {
            "cita_id": cita_id,
            "medicamento": medicamento,
            "dosis": dosis,
            "frecuencia": frecuencia,
            "duracion": duracion
        }
        
    }
    status, data = service_request(sock, service, datos)
    print_ins_del_upd(status, data)
    if status == 'OK':
        print("Receta creada con éxito.")
        sock.close()
        sys.exit()
    else:
        print(f"Error al crear la Receta: {data}.")

def leer_receta(sock,service):
    print("\n[ - Leer Receta - ]")
    id = input("Ingrese el id de la receta: ")
    datos = {
        "leer":"some",
        "id": id
        
    }
    status, data = service_request(sock, service, datos)
    print_select(status, data)
    if status == 'OK':
        print("Receta mostrada con éxito.")
        sock.close()
        sys.exit()
    else:
        print(f"Error al crear la Receta: {data}.")

def eliminar_receta(sock,service):
    print("\n[ - Eliminar Receta - ]")
    id = input("Ingrese el id de la receta: ")
    datos = {
        "eliminar":"some",
        "id": id
        
    }
    status, data = service_request(sock, service, datos)
    print_ins_del_upd(status, data)
    if status == 'OK':
        print("Receta eliminada con éxito.")
        sock.close()
        sys.exit()
    else:
        print(f"Error al crear la Receta: {data}.")

def leer_recetas_paciente(sock,service):
    session = get_session()
    print("\n[ - Leer Mis Recetas - ]")
    print("[1] Leer mis recetas por cita.")
    print("[2] Leer mis ultimas 10 recetas.")
    opcion = input_field("Su elección: ", max_length=1)
    if opcion == '1':
        cita_id = input_field("Ingrese el ID de la cita: ", max_length=10)
        datos = {
            "leer": "some",
            "cita_id": cita_id,
            "rut_paciente": session['rut']
        }
        status, data = service_request(sock, service, datos)
        print_select(status, data)
        if status == 'OK':
            print("Recetas mostradas con éxito.")
            sock.close()
            sys.exit()
        else:
            print(f"Error al crear la Receta: {data}.")
        
    elif opcion == '2':
        datos = {
            "leer":"some",
            "rut_paciente": session['rut']
            
        }
        status, data = service_request(sock, service, datos)
        print_select(status, data)
        if status == 'OK':
            print("Receta mostradas con éxito.")
            sock.close()
            sys.exit()
        else:
            print(f"Error al crear la Receta: {data}.")

def print_menu_medico():
    print("\n[ - Servicio de Recetas/Medicamentos (Médico) - ]")
    print("[1] Crear receta.")
    print("[2] Leer Receta.")
    print("[3] Eliminar Receta.")
    print("[0] Salir.")
    

def print_menu_paciente():
    print("\n[ - Servicio de Recetas/Medicamentos (Paciente) - ]")
    print("[1] Leer Mis Ultimas recetas.")
    print("[0] Salir.")
    



def main_client():
    service = 'recip'
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
                        crear_receta(sock=sock,service= service)
                    elif choice == '2':
                        leer_receta(sock=sock,service= service)
                    
                    elif choice == '3':
                        eliminar_receta(sock=sock,service= service)
                    else:
                        print("Opción no válida. Intente de nuevo.")
                        
            elif session['rol']=='':
                while True:
                    print_menu_paciente()
                    choice = input_field("Ingrese el número de la opción que desea ejecutar: ", max_length=1)
                    if choice == '0':
                        break
                    elif choice == '1':
                        leer_receta(sock=sock,service= service)
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