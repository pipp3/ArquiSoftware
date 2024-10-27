import os
from client import get_session


def print_menu():
    print("Seleccione un archivo para ejecutar:")
    print("1. Servicio de manejo de usuarios")



def execute_file(file_path):
    try:
        os.system(f"python3 {file_path}")
    except Exception as e:
        print(f"Error al ejecutar el archivo {file_path}: {e}")


if __name__ == "__main__":
    execute_file("user_login.py")
    session = get_session()
    if 'cargo' not in session or session['cargo'] == 'admin':
        while True: 
            print_menu()
            choice = input("Ingrese el número del archivo que desea ejecutar (0 para salir): ")

            if choice == '0':
                break
            elif choice.isdigit() and 1 <= int(choice) <= 8:
                file_name = [
                    "user_management.py"
                ][int(choice) - 1]
                # Si es necesario se podria de  aqui mismo iniciar el servicio tambien
                execute_file(file_name)
            else:
                print("Opción no válida. Intente de nuevo.")
    if 'cargo' not in session or session['cargo'] == 'medico':
        while True:
            #print_menu2()
            choice = input("Ingrese el número del archivo que desea ejecutar (0 para salir): ")

            if choice == '0':
                break
            elif choice.isdigit() and 1 <= int(choice) <= 8:
                file_name = [
                    "asign_block.py",
                    "comment.py",
                ][int(choice) - 1]
                # Si es necesario se podria de aqui mismo iniciar el servicio tambien
                execute_file(file_name)
            else:
                print("Opción no válida. Intente de nuevo.")

