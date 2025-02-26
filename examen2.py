import os
import platform
# Aerolinea LASER - Proyecto de Programacion I
# Jose Antonio Velasquez C.I: 31.571.901
#Jhonny Ferrer C.I: 31.257.319

# Variables globales para almacenar los totales
total_boletos = 0
total_primera = 0.0
total_segunda = 0.0
total_tercera = 0.0
total_nacional = 0.0
total_internacional = 0.0
total_servicios = 0

# Variables para rutas nacionales (precios fijos de la tabla)
total_porlamar_caracas = 0.0
total_caracas_porlamar = 0.0
total_puerto_ordaz_caracas = 0.0
total_caracas_puerto_ordaz = 0.0
total_maracaibo_caracas = 0.0
total_caracas_maracaibo = 0.0
total_elvigia_caracas = 0.0
total_caracas_elvigia = 0.0
total_barcelona_caracas = 0.0
total_caracas_barcelona = 0.0
total_lafria_caracas = 0.0
total_caracas_lafria = 0.0

# Variables para rutas internacionales
total_bogota = 0.0
total_curazao = 0.0
total_santo_domingo = 0.0
total_la_romana = 0.0

def limpiar_consola():
    sistema = platform.system()
    if sistema == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


def obtener_entero_valido(mensaje, minimo=0):
    """Valida que el usuario ingrese un numero entero mayor o igual al minimo"""
    while True:
        try:
            valor = int(input(mensaje))
            if valor >= minimo:
                return valor
            print(f"¡Error! Debe ser al menos {minimo}")
        except ValueError:
            print("¡Error! Ingrese un numero valido")

def obtener_decimal_valido(mensaje):
    """Valida que el usuario ingrese un numero decimal"""
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("¡Error! Ingrese un monto valido")
            

def seleccionar_ruta_nacional():
    """Muestra opciones de rutas nacionales y devuelve el precio y nombre de la ruta"""
    print("\nRutas nacionales disponibles:")
    print("1. Porlamar - Caracas ($505)")
    print("2. Caracas - Porlamar ($505)")
    print("3. Puerto Ordaz - Caracas ($455)")
    print("4. Caracas - Puerto Ordaz ($455)")
    print("5. Maracaibo - Caracas ($805)")
    print("6. Caracas - Maracaibo ($805)")
    print("7. El Vigia - Caracas ($755)")
    print("8. Caracas - El Vigia ($755)")
    print("9. Barcelona - Caracas ($305)")
    print("10. Caracas - Barcelona ($305)")
    print("11. La Fria - Caracas ($605)")
    print("12. Caracas - La Fria ($605)")
    
    while True:
        opcion = input("Seleccione la ruta (1-12): ")
        if opcion in {'1','2','3','4','5','6','7','8','9','10','11','12'}:
            break
        print("¡Error! Opcion no valida")
    
    # Asignar precio y nombre de ruta segun opcion
    if opcion == '1':
        return 505, "Porlamar - Caracas"
    elif opcion == '2':
        return 505, "Caracas - Porlamar"
    elif opcion == '3':
        return 455, "Puerto Ordaz - Caracas"
    elif opcion == '4':
        return 455, "Caracas - Puerto Ordaz"
    elif opcion == '5':
        return 805, "Maracaibo - Caracas"
    elif opcion == '6':
        return 805, "Caracas - Maracaibo"
    elif opcion == '7':
        return 755, "El Vigia - Caracas"
    elif opcion == '8':
        return 755, "Caracas - El Vigia"
    elif opcion == '9':
        return 305, "Barcelona - Caracas"
    elif opcion == '10':
        return 305, "Caracas - Barcelona"
    elif opcion == '11':
        return 605, "La Fria - Caracas"
    else: # opcion 12
        return 605, "Caracas - La Fria"

def seleccionar_ruta_internacional():
    """Valida el destino internacional y devuelve el nombre de la ruta"""
    destinos = ["Bogota", "Curazao", "Santo Domingo", "La Romana"]
    while True:
        destino = input("Destino internacional (Bogota/Curazao/Santo Domingo/La Romana): ").strip().title()
        if destino in destinos:
            return f"Caracas - {destino} (Ida y vuelta)"
        print("¡Destino no disponible! Elija entre Bogota, Curazao, Santo Domingo o La Romana")

def aplicar_clase(precio_base, clase):
    """Ajusta el precio segun la clase seleccionada"""
    if clase == '1':
        return precio_base * 2  # Primera clase: +100%
    elif clase == '2':
        return precio_base * 1.5  # Segunda clase: +50%
    else:
        return precio_base  # Tercera clase: precio base

def validar_edad_con_acompanante():
    """Permite menores solo si un adulto esta presente"""
    edad = obtener_entero_valido("Edad del pasajero: ", 1)  # Edad minima 1 año
    
    if edad < 18:
        print("\n[!] Menor detectado. Se requiere un adulto en la misma compra")
        # Validar que al menos un boleto sea de adulto
        while True:
            adultos = obtener_entero_valido("Numero de adultos en esta compra (al menos 1): ", 1)
            if adultos >= 1:
                return edad
            print("¡Error! Debe haber al menos un adulto")
    return edad

def validar_nombre(mensaje):
    """Valida que el nombre solo contenga letras y espacios."""
    while True:
        nombre = input(mensaje).strip()
        if all(caracter.isalpha() or caracter.isspace() for caracter in nombre):
            return nombre
        print("¡Error! El nombre solo puede contener letras y espacios")

def procesar_boleto():
    """Procesa la venta de un boleto individual"""
    global total_boletos, total_primera, total_segunda, total_tercera
    global total_nacional, total_internacional, total_servicios
    global total_porlamar_caracas, total_caracas_porlamar, total_puerto_ordaz_caracas, total_caracas_puerto_ordaz
    global total_maracaibo_caracas, total_caracas_maracaibo, total_elvigia_caracas, total_caracas_elvigia
    global total_barcelona_caracas, total_caracas_barcelona, total_lafria_caracas, total_caracas_lafria
    global total_bogota, total_curazao, total_santo_domingo, total_la_romana

    # Datos del pasajero
    nombre = validar_nombre("\nNombre del pasajero: ")
    
    # Validar tipo de cedula (V/E)
    while True:
        cedula = input("Tipo de cedula (V/E): ").upper()
        if cedula in ('V', 'E'):
            break
        print("¡Error! Ingrese V o E")
    
    # Validar edad (>=18)
    edad = validar_edad_con_acompanante()
    
    # Validar clase (1,2,3) y restriccion de tercera clase
    while True:
        clase = input("Clase (1: Primera, 2: Segunda, 3: Tercera): ")
        if clase in ('1', '2', '3'):
            if clase == '3' and edad >= 60:
                print("¡Error! Tercera clase no disponible para mayores de 60")
            else:
                break
        print("¡Error! Ingrese 1, 2 o 3")
    
    # Validar tipo de boleto (N/I)
    while True:
        tipo = input("Tipo de boleto (N: Nacional, I: Internacional): ").upper()
        if tipo in ('N', 'I'):
            break
        print("¡Error! Ingrese N o I")
    
    # Procesar ruta y precio
    precio = 0
    ruta = ""
    if tipo == 'N':
        precio_base, ruta = seleccionar_ruta_nacional()
        precio = aplicar_clase(precio_base, clase)
    else:
        ruta = seleccionar_ruta_internacional()
        # Precios internacionales segun clase
        if clase == '1':
            precio = 1000  # Ejemplo: Precios ajustados
        elif clase == '2':
            precio = 800
        else:
            precio = 600
    
    # Aplicar descuento por edad
    if edad < 12 or edad >= 60:
        precio *= 0.9
    
    # Servicios adicionales
    servicios = input("¿Requiere servicios adicionales? (S/N): ").upper()
    if servicios == 'S':
        total_servicios += 1
    
    # Actualizar totales
    total_boletos += 1
    if clase == '1':
        total_primera += precio
    elif clase == '2':
        total_segunda += precio
    else:
        total_tercera += precio
    
    if tipo == 'N':
        total_nacional += precio
        # Actualizar total por ruta nacional especifica
        if "Porlamar - Caracas" in ruta:
            total_porlamar_caracas += precio
        elif "Caracas - Porlamar" in ruta:
            total_caracas_porlamar += precio
        elif "Puerto Ordaz - Caracas" in ruta:
            total_puerto_ordaz_caracas += precio
        elif "Caracas - Puerto Ordaz" in ruta:
            total_caracas_puerto_ordaz += precio
        elif "Maracaibo - Caracas" in ruta:
            total_maracaibo_caracas += precio
        elif "Caracas - Maracaibo" in ruta:
            total_caracas_maracaibo += precio
        elif "El Vigia - Caracas" in ruta:
            total_elvigia_caracas += precio
        elif "Caracas - El Vigia" in ruta:
            total_caracas_elvigia += precio
        elif "Barcelona - Caracas" in ruta:
            total_barcelona_caracas += precio
        elif "Caracas - Barcelona" in ruta:
            total_caracas_barcelona += precio
        elif "La Fria - Caracas" in ruta:
            total_lafria_caracas += precio
        else:
            total_caracas_lafria += precio
    else:
        total_internacional += precio
        # Actualizar total por destino internacional
        if "Bogota" in ruta:
            total_bogota += precio
        elif "Curazao" in ruta:
            total_curazao += precio
        elif "Santo Domingo" in ruta:
            total_santo_domingo += precio
        else:
            total_la_romana += precio
    
    # Procesar pago
    print(f"\nTotal a pagar: ${precio:.2f}")
    while True:
        pago = obtener_decimal_valido("Ingrese el monto pagado: $")
        if pago >= precio:
            print(f"Vuelto: ${pago - precio:.2f}")
            break
        print("¡Monto insuficiente! Ingrese un valor mayor")

def mostrar_reporte():
    """Muestra el reporte de ventas"""
    print("\n--- REPORTE DE VENTAS ---")
    print(f"Total boletos vendidos: {total_boletos}")
    print("\nIngresos por clase:")
    print(f"Primera clase: ${total_primera:.2f}")
    print(f"Segunda clase: ${total_segunda:.2f}")
    print(f"Tercera clase: ${total_tercera:.2f}")
    print("\nIngresos por tipo:")
    print(f"Nacional: ${total_nacional:.2f}")
    print(f"Internacional: ${total_internacional:.2f}")
    print("\nIngresos por rutas nacionales:")
    print(f"Porlamar-Caracas: ${total_porlamar_caracas:.2f}")
    print(f"Caracas-Porlamar: ${total_caracas_porlamar:.2f}")
    print(f"Puerto Ordaz-Caracas: ${total_puerto_ordaz_caracas:.2f}")
    print(f"Caracas-Puerto Ordaz: ${total_caracas_puerto_ordaz:.2f}")
    print(f"Maracaibo-Caracas: ${total_maracaibo_caracas:.2f}")
    print(f"Caracas-Maracaibo: ${total_caracas_maracaibo:.2f}")
    print(f"El Vigia-Caracas: ${total_elvigia_caracas:.2f}")
    print(f"Caracas-El Vigia: ${total_caracas_elvigia:.2f}")
    print(f"Barcelona-Caracas: ${total_barcelona_caracas:.2f}")
    print(f"Caracas-Barcelona: ${total_caracas_barcelona:.2f}")
    print(f"La Fria-Caracas: ${total_lafria_caracas:.2f}")
    print(f"Caracas-La Fria: ${total_caracas_lafria:.2f}")
    print("\nIngresos por destinos internacionales:")
    print(f"Bogota: ${total_bogota:.2f}")
    print(f"Curazao: ${total_curazao:.2f}")
    print(f"Santo Domingo: ${total_santo_domingo:.2f}")
    print(f"La Romana: ${total_la_romana:.2f}")
    print(f"\nServicios adicionales solicitados: {total_servicios}")

def main():
    """Funcion principal que maneja el menu."""
    while True:
        print("\n=== AEROLiNEA LASER ===")
        print("1. Comprar boleto")
        print("2. Ver reporte del sistema")
        print("3. Salir")
        opcion = input("Seleccione una opcion: ")
        
        if opcion == '1':
            limpiar_consola()
            boletos = obtener_entero_valido("\nNumero de boletos a comprar: ", 1)
            for _ in range(boletos):
                procesar_boleto()
        elif opcion == '2':
            limpiar_consola()
            mostrar_reporte()
        elif opcion == '3':
            print("¡Gracias por usar nuestro sistema!")
            break
        else:
            print("¡Opcion invalida! Intente nuevamente")

if __name__ == "__main__":
    main()