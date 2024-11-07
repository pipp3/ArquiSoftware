import os
import sys
from client import get_session

def print_menu_admin():
    print("\nMenú de Administrador:")
    print("1. Servicio de manejo de usuarios")
    print("2. Servicio de comentarios")
    print("0. Salir")

def print_menu_paciente():
    print("\nMenú de Paciente:")
    print("1. Servicio de comentarios")
    print("0. Salir")

def execute_file(file_path):
    try:
        os.system(f"python3 {file_path}")
    except Exception as e:
        print(f"Error al ejecutar el archivo {file_path}: {str(e)}")

def handle_admin_menu():
    while True:
        print_menu_admin()
        choice = input("Ingrese el número del archivo que desea ejecutar: ")
        
        if choice == '0':
            break
        
        files = {
            '1': 'user_management.py',
            '2': 'comment.py'
        }
        
        if choice in files:
            execute_file(files[choice])
        else:
            print("Opción no válida. Intente de nuevo.")

def handle_paciente_menu():
    while True:
        print_menu_paciente()
        choice = input("Ingrese el número del archivo que desea ejecutar: ")
        
        if choice == '0':
            break
        
        if choice == '1':
            execute_file('comment.py')
        else:
            print("Opción no válida. Intente de nuevo.")

def main():
    # Uncomment if needed for password/user reset
    # execute_file("register.py")
    
    execute_file("user_login.py")
    session = get_session()
    
    if not session or 'cargo' not in session:
        print("No se ha iniciado sesión correctamente.")
        sys.exit(1)
    
    if session['cargo'] == 'admin':
        handle_admin_menu()
    elif session['cargo'] == 'paciente':
        handle_paciente_menu()
    else:
        print(f"Tipo de usuario no reconocido: {session['cargo']}")
        sys.exit(1)

if __name__ == "__main__":
    main()
