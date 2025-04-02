import os
import re
from datetime import datetime

# Constantes aeiou
PRECIOS = {
    'FAMILY ROOM': 200,
    'SENCILLA': 60,
    'DOBLE': 120,
    'SUITE': 300
}

ARCHIVOS = {
    'Individual': 'individual.txt',
    'Acompañado': 'acompañado.txt',
    'Grupo/Familia': 'grupo_familia.txt'
}

# Utilidades
def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def presionar_continuar():
    input("\nPresione Enter para continuar...")

# Validaciones
def validar_numero(mensaje):
    while True:
        entrada = input(mensaje)
        if entrada.isdigit():
            return int(entrada)
        print("Error: Debe ingresar un numero valido")

def validar_email(mensaje):
    regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    while True:
        email = input(mensaje)
        if re.match(regex, email):
            return email
        print("Email invalido. Intente nuevamente")

# Manejo de archivos TXT
def cargar_registros(tipo):
    registros = []
    try:
        with open(ARCHIVOS[tipo], 'r', encoding='utf-8') as f:
            contenido = f.read().split('\n\n')
            for bloque in contenido:
                if bloque.strip():
                    registro = {}
                    lineas = bloque.split('\n')
                    for linea in lineas:
                        if ': ' in linea:
                            clave, valor = linea.split(': ', 1)
                            registro[clave] = valor
                    registros.append(registro)
    except FileNotFoundError:
        pass
    return registros

def guardar_registros(tipo, registros):
    with open(ARCHIVOS[tipo], 'w', encoding='utf-8') as f:
        for registro in registros:
            bloque = '\n'.join([f"{k}: {v}" for k, v in registro.items()])
            f.write(bloque + '\n\n')

# Funciones para tipos de reserva
def capturar_datos_persona(num_persona=None):
    datos = {}
    prefijo = f"Acompañante {num_persona} - " if num_persona else ""
    
    datos[f'{prefijo}Nombre'] = input(f"{prefijo}Nombre: ")
    datos[f'{prefijo}Apellido'] = input(f"{prefijo}Apellido: ")
    datos[f'{prefijo}Cedula'] = str(validar_numero(f"{prefijo}Cedula: "))
    datos[f'{prefijo}Email'] = validar_email(f"{prefijo}Email: ")
    datos[f'{prefijo}Telefono'] = str(validar_numero(f"{prefijo}Telefono: "))
    return datos

def registrar_acompaniado():
    limpiar_pantalla()
    print("\nRegistro de cliente (Acompañado)")
    registro = {}
    registro.update(capturar_datos_persona())
    registro.update(capturar_datos_persona(1))
    return registro

def registrar_grupo_familia():
    limpiar_pantalla()
    print("\nRegistro de Grupo/Familia")
    registro = {}
    
    num_adultos = validar_numero("Cantidad de adultos: ")
    for i in range(1, num_adultos+1):
        registro.update(capturar_datos_persona(i))
    
    if input("¿Tiene hijos? (s/n): ").lower() == 's':
        num_hijos = validar_numero("Cantidad de hijos: ")
        for i in range(1, num_hijos+1):
            registro[f'Hijo {i} - Nombre'] = input(f"Hijo {i} - Nombre: ")
            registro[f'Hijo {i} - Apellido'] = input(f"Hijo {i} - Apellido: ")
            registro[f'Hijo {i} - Edad'] = str(validar_numero(f"Hijo {i} - Edad: "))
    
    return registro

# Operaciones post-registro
def mostrar_resumen(registro, tipo, total):
    limpiar_pantalla()
    print("\n=== RESUMEN DE RESERVA ===")
    print(f"Tipo: {tipo}")
    print(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    
    for clave, valor in registro.items():
        if not clave.startswith('Hijo') and not clave.startswith('Acompañante'):
            print(f"{clave}: {valor}")
    
    print(f"\nTotal a pagar: ${total}")
    presionar_continuar()

def menu_post_registro(tipo, registros, current_index):
    index = current_index  # indice dinamico para navegacion
    while True:
        limpiar_pantalla()
        print("\n=== OPCIONES ADICIONALES ===")
        print(f"Registro actual: {index + 1} de {len(registros)}")
        print("1. Ver cliente anterior")
        print("2. Ver cliente siguiente")
        print("3. Buscar cliente")
        print("4. Añadir mas clientes")
        print("5. Modificar datos")
        print("6. Finalizar operacion")
        
        opcion = input("Seleccione una opcion: ")
        
        if opcion == '1':
            if index > 0:
                index -= 1 
                mostrar_resumen(registros[index], tipo, registros[index]['Total'])
            else:
                print("No hay registros anteriores")
        
        elif opcion == '2':
            if index < len(registros) - 1:
                index += 1
                mostrar_resumen(registros[index], tipo, registros[index]['Total'])
            else:
                print("No hay registros siguientes")
        
        elif opcion == '3':
            buscar_cliente(tipo)
        
        elif opcion == '4':
            return True
        
        elif opcion == '5':
            modificar_registro(tipo, registros, index)
        
        elif opcion == '6':
            return False
        
        else:
            print("Opcion invalida")
        
        presionar_continuar()

def buscar_cliente(tipo):
    limpiar_pantalla()
    termino = input("Ingrese nombre, apellido o cedula para buscar: ").lower()
    registros = cargar_registros(tipo)
    
    resultados = []
    for registro in registros:
        for valor in registro.values():
            if termino in str(valor).lower():
                resultados.append(registro)
                break
    
    if resultados:
        print(f"\nSe encontraron {len(resultados)} resultados:")
        for i, res in enumerate(resultados, 1):
            print(f"{i}. {res.get('Nombre', '')} {res.get('Apellido', '')}")
    else:
        print("No se encontraron resultados")
    
    presionar_continuar()

def modificar_registro(tipo, registros, index):
    registro = registros[index]
    print("\nCampos disponibles:")
    campos = list(registro.keys())
    
    for i, campo in enumerate(campos, 1):
        print(f"{i}. {campo}")
    
    opcion = validar_numero("Seleccione campo a modificar: ") - 1
    if 0 <= opcion < len(campos):
        nuevo_valor = input(f"Nuevo valor para {campos[opcion]}: ")
        registro[campos[opcion]] = nuevo_valor
        guardar_registros(tipo, registros)
        print("Modificacion exitosa!")
    else:
        print("Opcion invalida")

# Flujo principal
def main():
    while True:
        limpiar_pantalla()
        print("=== LIDOTEL - Sistema de Reservas ===")
        print("1. Nuevo cliente")
        print("2. Salir")
        opcion = input("Seleccione una opcion: ")
        
        if opcion == '1':
            while True:
                limpiar_pantalla()
                print("\nTipo de reservacion:")
                print("1. Individual")
                print("2. Acompañado")
                print("3. Grupo/Familia")
                print("4. Volver")
                sub_opcion = input("Seleccione una opcion: ")
                
                if sub_opcion == '4':
                    break
                
                tipos = ['Individual', 'Acompañado', 'Grupo/Familia']
                if sub_opcion in ['1', '2', '3']:
                    tipo = tipos[int(sub_opcion)-1]
                    registros = cargar_registros(tipo)
                    
                    while True:
                        if tipo == 'Individual':
                            cliente = capturar_datos_persona()
                        elif tipo == 'Acompañado':
                            cliente = registrar_acompaniado()
                        else:
                            cliente = registrar_grupo_familia()
                        
                        dias = validar_numero("Dias de estadia: ")
                        
                        print("\nTipos de habitacion:")
                        for i, hab in enumerate(PRECIOS.keys(), 1):
                            print(f"{i}. {hab} - ${PRECIOS[hab]}/noche")
                        
                        opcion_hab = validar_numero("Seleccione habitacion: ") - 1
                        habitacion = list(PRECIOS.keys())[opcion_hab]
                        total = PRECIOS[habitacion] * dias
                        
                        cliente['Habitacion'] = habitacion
                        cliente['Dias'] = str(dias)
                        cliente['Total'] = str(total)
                        cliente['Fecha'] = datetime.now().strftime('%d/%m/%Y %H:%M')
                        
                        mostrar_resumen(cliente, tipo, total)
                        registros.append(cliente)
                        guardar_registros(tipo, registros)
                        
                        continuar = menu_post_registro(tipo, registros, len(registros)-1)
                        if not continuar:
                            break
                    
                    print("\n¡Gracias por utilizar nuestros servicios!")
                    presionar_continuar()
                
                else:
                    print("Opcion invalida")
        
        elif opcion == '2':
            print("\n¡Gracias por usar nuestro sistema!")
            break
        
        else:
            print("Opcion invalida")
            presionar_continuar()

if __name__ == "__main__":
    main()