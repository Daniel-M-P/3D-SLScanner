import cv2
import os
import glob

def obtener_imagenes_en_directorio(raiz):
    """
    Obtiene una lista de todas las imágenes en un directorio y subdirectorios.
    """
    tipos_imagen = ("*.png", "*.jpg", "*.jpeg", "*.bmp", "*.tiff")
    imagenes = []
    for extension in tipos_imagen:
        imagenes.extend(glob.glob(os.path.join(raiz, "**", extension), recursive=True))
    return sorted(imagenes)

def mostrar_imagen_en_ventana_unica(imagen_path, ventana, titulo):
    """
    Muestra la imagen en una ventana única y actualiza el título.
    """
    imagen = cv2.imread(imagen_path)
    if imagen is not None:
        cv2.imshow(ventana, imagen)
        cv2.setWindowTitle(ventana, titulo)
    else:
        print(f"No se pudo cargar la imagen: {imagen_path}")

def obtener_titulo(imagen_path, directorio_raiz):
    """
    Genera el título de la ventana a partir del path de la imagen.
    """
    relativo = os.path.relpath(imagen_path, directorio_raiz)
    return f"Visualizando: {relativo}"

def recorrer_imagenes(directorio_raiz):
    """
    Recorre todas las imágenes dentro de un directorio base usando una sola ventana.
    """
    imagenes = obtener_imagenes_en_directorio(directorio_raiz)
    if not imagenes:
        print("No se encontraron imágenes en el directorio.")
        return

    idx = 0
    ventana = "Visualizador de Imágenes"
    cv2.namedWindow(ventana, cv2.WINDOW_AUTOSIZE)

    while True:
        if idx >= len(imagenes):
            print("Se han visualizado todas las imágenes.")
            break

        imagen_path = imagenes[idx]
        titulo = obtener_titulo(imagen_path, directorio_raiz)
        mostrar_imagen_en_ventana_unica(imagen_path, ventana, titulo)

        # Espera por la tecla presionada
        key = cv2.waitKey(0)

        if key == 27:  # Tecla ESC para salir
            print("Cerrando visualizador.")
            break
        elif key == ord('d'):  # Letra D para avanzar
            idx += 1
        else:
            print("Usa la letra 'D' para avanzar o ESC para salir.")

    cv2.destroyAllWindows()

# Pregunta al usuario en qué directorio buscar
print("Selecciona el directorio base para buscar imágenes.")
directorio_base = os.path.dirname(os.path.abspath(__file__))
print(f"Directorio actual: {directorio_base}")

directorio_relativo = input("Ingresa el nombre del directorio (o presiona Enter para usar el actual): ").strip()
if directorio_relativo:
    directorio_raiz = os.path.join(directorio_base, directorio_relativo)
else:
    directorio_raiz = directorio_base

if not os.path.isdir(directorio_raiz):
    print(f"El directorio '{directorio_raiz}' no existe.")
else:
    recorrer_imagenes(directorio_raiz)
