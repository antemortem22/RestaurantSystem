import time
import os
import sqlite3

# Verificar si el archivo de la base de datos existe
if not os.path.exists("comercio.sqlite"):
    # Crear la conexión a la base de datos y el archivo si no existe
    conn = sqlite3.connect("comercio.sqlite")
    conn.close()

# Configuración SQLite
conn = sqlite3.connect("comercio.sqlite")
cursor = conn.cursor()
cursor.executescript("CREATE TABLE IF NOT EXISTS registro (id INT, encargado TEXT, fecha TEXT, evento TEXT, caja REAL)")
cursor.executescript("CREATE TABLE IF NOT EXISTS ventas (id INT, cliente TEXT, fecha TEXT, combo_S INT, combo_D INT, combo_T INT, flurby INT, total REAL)")

# Definición de variables
caja_encargado = 0
opcion = ""
encargadoactual = ""
nombre_cliente = ""
total = 0
cantidad_flurby = 0
cantidad_combo_t = 0
cantidad_combo_d = 0
cantidad_combo_s = 0
incrementarID_ingreso = 0
incrementarID_venta=0
confirmar = ""

# Definición de funciones

###Incremeta el ID de la tabla INGRESOS
def incrementar_ingreso():
    global incrementarID_ingreso
    incrementarID_ingreso += 1
    return incrementarID_ingreso
###Incremeta el ID de la tabla INGRESOS
def incrementar_venta():
    global incrementarID_venta
    incrementarID_venta += 1
    return incrementarID_venta

###Funcion que muestra el encargado, el menu y permite elegir una opcion del menu  
def ingresar_opcion():
    global opcion, encargadoactual
    print("\nBienvenido a Hamburguesas IT")
    print("Encargad@ ->", encargadoactual)
    print("Recuerda, siempre hay que recibir al cliente con una sonrisa :)\n")
    print("##### MENU #####")
    print("1 - Ingresar nuevo pedido")
    print("2 - Cambio de turno") 
    print("3 - Apagar sistema")
    opcion = input("Ingrese la opcion que desea ejecutar: \n -->")
    print("############################################")

###Funcion para ingresar pedidos mostrando las opciones, el cliente, el total, la paga y el vuelto
def ingresar_pedido():  
    global nombre_cliente, cantidad_combo_s, cantidad_combo_d, cantidad_combo_t, cantidad_flurby, total, caja_encargado, confirmar
    while True:
        nombre_cliente = input("Ingrese nombre del cliente: ")
        if nombre_cliente == "" or not nombre_cliente.isalpha():
            print("La información ingresada no es válida. Por favor, ingrese solo letras.")
        else:
            break

    while True:
        cantidad_combo_s = input("Ingrese cantidad Combo S: ")
        
        if cantidad_combo_s == "" or not cantidad_combo_s.isdecimal():
            print("Los valores ingresados no son validos, por favor, ingrese numeros") 
        else:
            break 
    cantidad_combo_s = int(cantidad_combo_s) 

    while True:
        cantidad_combo_d = input("Ingrese cantidad Combo D: ")
        if cantidad_combo_d == "" or not cantidad_combo_d.isdecimal():
            print("Los valores ingresados no son validos, por favor, ingrese numeros")
        else:
            break
    cantidad_combo_d = int(cantidad_combo_d)

    while True:
        cantidad_combo_t = input("Ingrese cantidad Combo T: ")
        if cantidad_combo_t == "" or not cantidad_combo_t.isdecimal():
            print("Los valores ingresados no son validos, por favor, ingrese numeros")
        else:
            break
    cantidad_combo_t = int(cantidad_combo_t)

    while True:
        cantidad_flurby = input("Ingrese cantidad de Flurby: ")
        if cantidad_flurby == "" or not cantidad_flurby.isdecimal():
            print("Los valores ingresados no son validos, por favor, ingrese numeros")
        else:
            break
    cantidad_flurby = int(cantidad_flurby)
    
    total = (cantidad_combo_s * 5) + (cantidad_combo_d * 6) + (cantidad_combo_t * 7) + (cantidad_flurby * 2)
    print("Total a pagar $", total)
    
    while True:
        pago = input("Ingrese monto del cliente: ")
        if not pago.isdigit():
            print("La entrada no es un número. Ingréselo de nuevo.")
        else:
            pago = float(pago)
            break
    
    vuelto = pago - total
    print("El vuelto es $", vuelto)
    
    while True:
        confirmar = input("¿Confirmar pedido? Y/N \n -->")
        if confirmar.lower() == "n":
            print("Pedido cancelado")
            return
        elif confirmar.lower() == "y":
            print("Pedido confirmado")
            caja_encargado += total
            break
        else:
            print("Opción inválida. Ingrese 'Y' para confirmar o 'N' para cancelar.")

###Pantalla inicial donde se pide nombre del encargado
def initial_screen():
    global encargadoactual
    print("Bienvenido a Hamburguesas IT")
    while True:
        encargadoactual = input("Ingrese su nombre, encargad@: \n -->" )
        if encargadoactual == "" or not encargadoactual.isalpha():
            print("La información ingresada no es válida. Por favor, ingrese solo letras.")
        else:
            break

###Guarda una grilla del empleado que ingreso
def guardar_ingreso():
    global encargadoactual, incrementarID_ingreso
    incrementar_ingreso()
    cursor.execute(f"INSERT INTO registro VALUES('{incrementarID_ingreso}','{encargadoactual}', '{time.asctime()}', 'IN', '{caja_encargado}')")
    conn.commit()

###Guarda una grilla del empleado que egreso
def guardar_egreso():
    global encargadoactual,incrementarID_ingreso
    incrementar_ingreso()
    cursor.execute(f"INSERT INTO registro VALUES('{incrementarID_ingreso}','{encargadoactual}', '{time.asctime()}', 'OUT', '{caja_encargado}')")
    conn.commit()

###Guarda una grilla con las ventas realizadas
def guardar_venta():
    global incrementarID_venta, confirmar
    incrementar_venta()
    if confirmar == "y":
        cursor.execute(f"INSERT INTO ventas VALUES('{incrementarID_venta}','{nombre_cliente}', '{time.asctime()}', '{cantidad_combo_s}', '{cantidad_combo_d}', '{cantidad_combo_t}', '{cantidad_flurby}', '{total}')")
        conn.commit()
    else:
        pass
   

# Inicio del bucle


if os.name == "nt":
    borrar = "cls"
else:
    borrar = "clear" 
os.system(borrar)

def main():
    os.system("cls")
    initial_screen()
    guardar_ingreso()
    os.system("cls")
    while True:
        ingresar_opcion()
        if opcion == "1":
            os.system("cls")
            ingresar_pedido()
            guardar_venta() 
            print("############################################")
        elif opcion == "2":
            os.system("cls")
            guardar_egreso()
            initial_screen()
            print("############################################")
        elif opcion == "3":
            break
        else:
            
            print("La opción ingresada no es válida, inténtelo de nuevo")
    os.system("cls")
    print("Saliendo de la app...\n¡Gracias por usarla!")

main()

conn.close()