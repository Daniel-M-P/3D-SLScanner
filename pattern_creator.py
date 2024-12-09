import cv2
import numpy as np
import math
import os

def generate_gray_code_patterns(resolution):
    # Desempaquetar resolución
    width, height = resolution

    # Calcular número de patrones necesarios para columnas y filas
    n_cols = math.ceil(math.log2(width)) 
    n_rows = math.ceil(math.log2(height)) 

    print(f"Número de patrones para columnas: {n_cols}")
    print(f"Número de patrones para filas: {n_rows}")

    # Generar patrones para las columnas
    col_patterns = []
    for bit in range(n_cols):
        pattern = np.zeros((height, width), dtype=np.uint8)
        for col in range(width):
            gray_code = col ^ (col >> 1)  # Generar Gray Code
            if gray_code & (1 << bit):  # Checar el bit actual
                pattern[:, col] = 255  # Blanco
        if np.any(pattern):  # Excluir patrón completamente negro
            col_patterns.append(pattern)


    # Generar patrones para las filas
    row_patterns = []
    for bit in range(n_rows):
        pattern = np.zeros((height, width), dtype=np.uint8)
        for row in range(height):
            gray_code = row ^ (row >> 1)  # Generar Gray Code
            if gray_code & (1 << bit):  # Checar el bit actual
                pattern[row, :] = 255  # Blanco
        if np.any(pattern):  # Excluir patrón completamente negro
            row_patterns.append(pattern)

    return col_patterns, row_patterns


def save_patterns(patterns, folder_name, prefix):
    folder_prefix = os.path.join(folder_name, prefix)
    if not os.path.exists(folder_prefix):
        os.makedirs(folder_prefix)
    for i in range(len(patterns)):
        pattern = patterns[len(patterns) - 1 - i]
        inverted_pattern = cv2.bitwise_not(pattern)
        filename = os.path.join(folder_prefix, f"{prefix}_pattern_{i*2}.png")
        cv2.imwrite(filename, pattern)
        if prefix != "full":
            filename_inverted = os.path.join(folder_prefix, f"{prefix}_pattern_{i*2 +1}.png")
            cv2.imwrite(filename_inverted, inverted_pattern)

if __name__ == "__main__":
    # Solicitar acción del usuario (guardar o cargar patrones)
    action = input("¿Quieres cargar los patrones desde una carpeta existente o crearlos en una nueva? (existente/nueva): ").strip().lower()

    if action == "existente":
        folder_name = input("Introduce el nombre de la carpeta existente: ").strip()

    elif action == "nueva":
        folder_name = input("Introduce el nombre de la nueva carpeta: ").strip()
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        # Solicitar la resolución de la pantalla
        width = int(input("Introduce el ancho del proyector en píxeles: "))
        height = int(input("Introduce el alto del proyector en píxeles: "))
        col_patterns, row_patterns = generate_gray_code_patterns((width, height))
        full = [np.zeros((height, width), dtype=np.uint8), np.full((height, width), 255, dtype=np.uint8)]

        # Guardar patrones si se especificó una carpeta
        save_patterns(col_patterns, folder_name, "column")
        save_patterns(row_patterns, folder_name, "row")
        save_patterns(full, folder_name, "full")
        print(f"Patrones guardados en la carpeta: {folder_name}")

    else:
        print("Opción no válida. Los patrones no serán guardados.")
        folder_name = None

