import os
import sys
from client import get_session

def print_menu_admin():
    print("\nMenú de Administrador:")
    print("1. Servicio de manejo de usuarios")
    print("2. Servicio de comentarios")
    print("3. Servicio de notificaciones")
    print("4. Servicio de agendamiento de horas")
    print("5. Servicio de cancelación de horas")
    print("6. Servicio de re-agendamiento de horas")
    print("0. Salir")

def print_menu_paciente():
    print("\nMenú de Paciente:")
    print("1. Servicio de comentarios")
    print("2. Servicio de historial médico")
    print("3. Servicio de notificaciones")
    print("4. Servicio de agendamiento de horas")
    print("5. Servicio de cancelación de horas")
    print("6. Servicio de re-agendamiento de horas")
    print("7. Servicio de recetas")
    print("0. Salir")

def print_menu_medico():
    print("\nMenú de Médico:")
    print("1. Servicio de historial médico")
    print("2. Servicio de notificaciones")
    print("3. Servicio de recetas")
    print("4. Servicio de re-agendamiento de horas")
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
            '2': 'comment.py',
            '3': 'notification.py',
            '4': 'schedule.py',
            '5': 'cancel.py',
            '6': 'reschedule.py'
        }
        
        if choice in files:
            execute_file(files[choice])
        else:
            print("Opción no válida. Intente de nuevo.")

def handle_medico_menu():
    while True:
        print_menu_medico()
        choice = input("Ingrese el número del archivo que desea ejecutar: ")
        
        if choice == '0':
            break
        
        files = {
            '1': 'medical_history.py',
            '2': 'notification.py',
            '3': 'recipes.py',
            '4': 'reschedule.py'
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
        elif choice == '2':
            execute_file('medical_history.py')
        elif choice == '3':
            execute_file('notification.py')
        elif choice == '4':
            execute_file('schedule.py')
        elif choice == '5':
            execute_file('cancel.py')
        elif choice == '6':
            execute_file('reschedule.py')
        elif choice == '7':
            execute_file('recipes.py')        
        
        else:
            print("Opción no válida. Intente de nuevo.")

def main():
    # Uncomment if needed for password/user reset
    #execute_file("register.py")
    
    execute_file("user_login.py")
    session = get_session()
    
    if not session or 'rut' not in session:
        print("No se ha iniciado sesión correctamente.")
        sys.exit(1)
    
    if session['rol'] == 'admin':
        handle_admin_menu()
    elif session['rol'] == 'medico':
        handle_medico_menu()
    elif 'rol' not in session or session['rol'] == '':
        handle_paciente_menu()
    else:
        print(f"Tipo de usuario no reconocido")
        sys.exit(1)

if __name__ == "__main__":
    main()
