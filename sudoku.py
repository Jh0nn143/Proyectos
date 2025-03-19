import os
from colorama import Fore, Back, Style, init

# Inicia el colorama para colores en consola
# "pip install colorama" para que funcione
# Si no esta instalado no va a funcionar
init(autoreset=True)

# Tablero inicial con pistas (30)
tablero_inicial = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

# Tablero resuelto
tablero_resuelto = [
    [5, 3, 4, 6, 7, 8, 9, 1, 2],
    [6, 7, 2, 1, 9, 5, 3, 4, 8],
    [1, 9, 8, 3, 4, 2, 5, 6, 7],
    [8, 5, 9, 7, 6, 1, 4, 2, 3],
    [4, 2, 6, 8, 5, 3, 7, 9, 1],
    [7, 1, 3, 9, 2, 4, 8, 5, 6],
    [9, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 6, 1, 7, 9]
]

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_tablero(tablero, pistas):
    celdas_erroneas = verificar_errores(tablero)
    # Encabezado de columnas
    print(Fore.YELLOW + "\n    1   2   3    4   5   6    7   8   9")
    print(Fore.WHITE + "  " + "=" * 39)
    
    for i in range(9):
        fila_str = Fore.YELLOW + f"{i+1} " + Fore.WHITE + "|"
        for j in range(9):
            # Ponerle colorcito a la celda
            if pistas[i][j] != 0:
                color = Fore.CYAN
            elif (i, j) in celdas_erroneas:
                color = Fore.RED
            else:
                color = Fore.WHITE
            
            valor = f" {tablero[i][j]} " if tablero[i][j] != 0 else "   "
            fila_str += color + valor
            
            # Separadores verticales
            if (j + 1) % 3 == 0 and j != 8:
                fila_str += Fore.LIGHTBLACK_EX + "||"
            else:
                fila_str += Fore.WHITE + "|"
        
        print(fila_str)
        
        # Separadores horizontales entre cuadrantes
        if (i + 1) % 3 == 0 and i != 8:
            print(Fore.WHITE + "  " + "-" * 39)
    print(Fore.WHITE + "  " + "=" * 39)
    print(Style.RESET_ALL)

def es_valido(tablero, fila, col, num):
    # Aqui no permite poner un numero "mal" asi que para que funcione
    # que se imprima los numeros en rojo se comenta ambas validaciones
    # para que se vea en el tablero el numero en rojo

    # Aqui se verifica la fila y columna
    # Si el numero ya existe en la fila o columna, no es valido
    if num in tablero[fila] or num in [tablero[i][col] for i in range(9)]:
        return False
    # Aqui se verifica el cuadrante 3x3
    # Si el numero ya existe en el cuadrante, no es valido
    inicio_fila, inicio_col = 3 * (fila // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if tablero[inicio_fila + i][inicio_col + j] == num:
                return False
    return True

def verificar_errores(tablero):
    errores = set()
    for i in range(9):
        for j in range(9):
            num = tablero[i][j]
            if num == 0:
                continue
            # Verifica la fila
            if tablero[i].count(num) > 1:
                errores.add((i, j))
            # Verifica la columna
            columna = [tablero[k][j] for k in range(9)]
            if columna.count(num) > 1:
                errores.add((i, j))
            # Verifica el cuadrante 3x3
            inicio_fila, inicio_col = 3 * (i // 3), 3 * (j // 3)
            contador = 0
            for x in range(3):
                for y in range(3):
                    if tablero[inicio_fila + x][inicio_col + y] == num:
                        contador += 1
            if contador > 1:
                errores.add((i, j))
    return errores

def comprobar_victoria(tablero, solucion):
    return tablero == solucion

def main():
    tablero = [fila.copy() for fila in tablero_inicial]
    pistas = [[1 if cell != 0 else 0 for cell in fila] for fila in tablero_inicial]
    
    while True:
        limpiar_pantalla()
        mostrar_tablero(tablero, pistas)
        
        if comprobar_victoria(tablero, tablero_resuelto):
            print(Fore.GREEN + "¡Felicidades! Has resuelto el Sudoku")
            break
        
        try:
            fila = input("\nIngresa la fila (1-9) o 'R' para rendirte: ").upper()
            if fila == 'R':
                limpiar_pantalla()
                print(Fore.RED + "Tablero resuelto:")
                mostrar_tablero(tablero_resuelto, pistas)
                break
            
            fila = int(fila) - 1
            col = int(input("Ingresa la columna (1-9): ")) - 1
            
            if not (0 <= fila <= 8 and 0 <= col <= 8):
                input(Fore.RED + "Posicion invalida. Presiona Enter para continuar")
                continue
            
            if pistas[fila][col] == 1:
                input(Fore.RED + "No puedes modificar una pista. Presiona Enter")
                continue
            
            num = input("Ingresa el numero (1-9) o 0 para borrar: ")
            if not num.isdigit():
                input(Fore.RED + "Entrada invalida. Presiona Enter")
                continue
            
            num = int(num)
            if num == 0:
                tablero[fila][col] = 0
                continue
            
            if not (1 <= num <= 9):
                input(Fore.RED + "Numero debe ser 1-9. Presiona Enter")
                continue
            
            if es_valido(tablero, fila, col, num):
                tablero[fila][col] = num
            else:
                input(Fore.RED + "Numero invalido segun reglas. Presiona Enter")
        
        except ValueError:
            input(Fore.RED + "Entrada invalida. Presiona Enter para continuar")

if __name__ == "__main__":
    main()