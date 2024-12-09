import cv2
import threading

# Inicializa las cámaras
cap1 = cv2.VideoCapture(1)  # Primera cámara
cap2 = cv2.VideoCapture(2)  # Segunda cámara

# Diccionario de propiedades disponibles
properties = {
    "BRILLO": cv2.CAP_PROP_BRIGHTNESS,
    "CONTRASTE": cv2.CAP_PROP_CONTRAST,
    "SATURACION": cv2.CAP_PROP_SATURATION,
    "HUE": cv2.CAP_PROP_HUE,
    "GANANCIA": cv2.CAP_PROP_GAIN,
    "EXPOSICION": cv2.CAP_PROP_EXPOSURE,
    "ENFOQUE": cv2.CAP_PROP_FOCUS,
    "FPS": cv2.CAP_PROP_FPS,
    "ANCHO": cv2.CAP_PROP_FRAME_WIDTH,
    "ALTO": cv2.CAP_PROP_FRAME_HEIGHT,
}

# Variable para controlar el bucle de las cámaras
running = True

# Función para mostrar las cámaras en tiempo real
def mostrar_camaras():
    global running
    while running:
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()

        if not ret1 or not ret2:
            print("Error al capturar imágenes de una o ambas cámaras.")
            break

        # Muestra las imágenes en ventanas separadas
        cv2.imshow("Cámara 1", frame1)
        cv2.imshow("Cámara 2", frame2)

        # Verifica si se presiona 's' para salir
        if cv2.waitKey(1) & 0xFF == ord('s'):
            running = False
            break

# Inicia el hilo para mostrar las cámaras
hilo_camaras = threading.Thread(target=mostrar_camaras)
hilo_camaras.start()

# Función para mostrar las propiedades actuales de ambas cámaras
def mostrar_propiedades():
    print("\nPropiedades actuales:")
    for nombre, prop in properties.items():
        valor1 = cap1.get(prop)
        valor2 = cap2.get(prop)
        print(f"{nombre} - Cámara 1: {valor1}, Cámara 2: {valor2}")
    print("Escribe el índice de la cámara (0 o 1), el nombre de la propiedad y el nuevo valor (ejemplo: 0 BRILLO 100)")
    print("Presiona 's' en la ventana de la cámara para salir.")

# Mostrar propiedades iniciales
mostrar_propiedades()

# Bucle para manejar los cambios de propiedades
while running:
    try:
        # Lee la entrada del usuario
        user_input = input(">> ").strip().upper()

        # Procesa el cambio de propiedades
        cam_index, nombre_prop, nuevo_valor = user_input.split()
        cam_index = int(cam_index)  # Índice de la cámara (0 o 1)
        nuevo_valor = float(nuevo_valor)  # Convierte el valor a flotante

        # Selecciona la cámara correspondiente
        if cam_index == 0:
            cam = cap1
        elif cam_index == 1:
            cam = cap2
        else:
            print("Índice de cámara inválido. Usa 0 o 1.")
            continue

        # Verifica si la propiedad existe
        if nombre_prop in properties:
            cam.set(properties[nombre_prop], nuevo_valor)
            print(f"{nombre_prop} de Cámara {cam_index + 1} cambiado a {nuevo_valor}")
        else:
            print(f"Propiedad {nombre_prop} no encontrada. Intenta nuevamente.")

    except ValueError:
        print("Entrada no válida. Usa el formato: ÍNDICE PROPIEDAD VALOR (ejemplo: 0 BRILLO 100)")

    # Mostrar propiedades actualizadas
    mostrar_propiedades()

# Libera los recursos y cierra las ventanas
cap1.release()
cap2.release()
cv2.destroyAllWindows()
