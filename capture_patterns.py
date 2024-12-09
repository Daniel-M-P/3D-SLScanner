import cv2
import numpy as np
import os
import time
import re

def extraer_numero(nombre_archivo):
    # Usar una expresión regular para buscar el número en el nombre del archivo
    return int(nombre_archivo.split("_")[-1].split(".")[0])

def setup_cameras():
    CAML = cv2.VideoCapture(1)  # Adjust camera indices if needed
    CAMR = cv2.VideoCapture(2)
    
    # Set camera properties based on README values
    for cap in [CAML, CAMR]:
        cap.set(cv2.CAP_PROP_EXPOSURE, -8.0)
        cap.set(cv2.CAP_PROP_BRIGHTNESS, 70.0)
    
    return CAML, CAMR

def center_window(window_name, img):
    screen = cv2.getWindowImageRect(window_name)
    screen_width = screen[2]
    screen_height = screen[3]
    img_height, img_width = img.shape[:2]
    
    x = (screen_width - img_width) // 2
    y = (screen_height - img_height) // 2
    
    cv2.moveWindow(window_name, x, y)

def capture_patterns_for_angle(angle, CAML, CAMR, parent_folder, pattern_folder):
    angle_folder = f"grados{angle}"
    
    # Create output directories for this angle
    for cam in ['cam1', 'cam2']:
        for pattern_type in ['full', 'column', 'row']:
            os.makedirs(f"{parent_folder}/{angle_folder}/{cam}/{pattern_type}", exist_ok=True)
    
    # Setup display window
    cv2.namedWindow("Pattern", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("Pattern", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    
    # Process patterns in order: full, column, row
    pattern_types = ['full', 'column', 'row']
    first_capture = True
    
    for pattern_type in pattern_types:
        pattern_path = os.path.join(pattern_folder, pattern_type)
        patterns = sorted(os.listdir(pattern_path), key = extraer_numero)
        
        for idx, pattern_file in enumerate(patterns):
            # Load and display pattern
            pattern = cv2.imread(os.path.join(pattern_path, pattern_file))
            cv2.imshow("Pattern", pattern)
            center_window("Pattern", pattern)
            
            # Wait longer for first capture
            if first_capture:
                print(f"Para la primera captura de {angle_folder}, presiona 's' cuando estés listo...")
                while True:
                    if cv2.waitKey(1) & 0xFF == ord('s'):
                        break
                first_capture = False
            else:
                cv2.waitKey(500)
            
            # Capture from both cameras
            ret1, frame1 = CAML.read()
            ret2, frame2 = CAMR.read()
            
            if ret1 and ret2:
                cv2.imwrite(f"{parent_folder}/{angle_folder}/cam1/{pattern_type}/{pattern_type}_{idx}.png", frame1)
                cv2.imwrite(f"{parent_folder}/{angle_folder}/cam2/{pattern_type}/{pattern_type}_{idx}.png", frame2)
            else:
                print(f"Failed to capture {pattern_type} pattern {idx} for {angle_folder}")
            
            time.sleep(0.2)

def main():
    CAML, CAMR = setup_cameras()
    parent_folder = input("Por favor, introduce el nombre de la carpeta para guardar las imágenes:").strip().lower()
    pattern_folder = input("Por favor, introduce el nombre de la carpeta de los patrones a usar:").strip().lower()

    
    try:
        for angle in range(180, 301, 60):
            if angle > 0:
                input(f"\nPor favor, gira la plataforma a {angle} grados y presiona Enter para continuar...")
            
            print(f"\nComenzando capturas para {angle} grados")
            capture_patterns_for_angle(angle, CAML, CAMR, parent_folder, pattern_folder)
            print(f"Capturas completadas para {angle} grados")
    
    finally:
        CAML.release()
        CAMR.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()