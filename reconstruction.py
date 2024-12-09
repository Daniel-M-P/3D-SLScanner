import numpy as np
import deca 

def calcular_rayos(pixelL, pixelR, CAML, CAMR):
    pixelL = np.array([pixelL[0], pixelL[1], 1])
    q_pixelL = np.linalg.inv(CAML.matrix).dot(pixelL)
    q_worldL = np.linalg.inv(CAML.rot).dot(q_pixelL) - np.linalg.inv(CAML.matrix).dot(CAML.tras) 
    dirL = CAML.rot.T.dot(q_pixelL) 
    dirL /= np.linalg.norm(dirL)

    pixelR = np.array([pixelR[0], pixelR[1], 1])
    q_pixelR = np.linalg.inv(CAMR.matrix).dot(pixelR)
    q_worldR = np.linalg.inv(CAMR.rot).dot(q_pixelR) - np.linalg.inv(CAMR.matrix).dot(CAMR.tras)
    dirR = CAMR.rot.T.dot(q_pixelR)
    dirR /= np.linalg.norm(dirR)

    return q_worldL, dirL, q_worldR, dirR

def punto_intermedio(p, u, q, v):
    # Diferencia entre orígenes
    w = p - q

    # Productos escalares necesarios
    a = np.dot(u, u)
    b = np.dot(u, v)
    c = np.dot(v, v)
    d = np.dot(u, w)
    e = np.dot(v, w)

    # Denominador común
    denom = b * b - a * c

    # Parámetros escalares s y t
    s = (d * c - b * e) / denom
    t = (b * d - a * e) / denom

    # Puntos más cercanos en cada rayo
    puntoL = p + s * u
    puntoR = q + t * v

    # Punto intermedio (promedio de los puntos más cercanos)
    punto_medio = (puntoL + puntoR) / 2
    return punto_medio
        
def guardar_nube_de_puntos_ply(nube_de_puntos, archivo_salida):
    with open(archivo_salida, 'w') as archivo:
        archivo.write("ply\n")
        archivo.write("format ascii 1.0\n")
        archivo.write(f"element vertex {len(nube_de_puntos)}\n")
        archivo.write("property float x\n")
        archivo.write("property float y\n")
        archivo.write("property float z\n")
        archivo.write("end_header\n")
        for punto in nube_de_puntos:
            archivo.write(f"{punto[0]} {punto[1]} {punto[2]}\n")


if __name__ == "__main__":
    CAML, CAMR, coordenadas_por_angulo = deca.main()

    # Generar nube de puntos
    nube_de_puntos = []

    # Cada graycode de cada ángulo debe generar solo un punto
    for angle in coordenadas_por_angulo.values():
        for graycode in angle.values():
            puntos_graycode = []
            # Se espera que haya solo un punto por graycode
            for pixelL in graycode[0]:
                for pixelR in graycode[1]:
                        # Calcular los orígenes y direcciones de los rayos
                    puntoL, dirL, puntoR, dirR = calcular_rayos(
                        pixelL, pixelR,
                        CAML, CAMR,
                    )

                    # Calcular el punto intermedio
                    punto = punto_intermedio(puntoL, dirL, puntoR, dirR)

        if puntos_graycode:
            punto_promedio = np.mean(np.array(puntos_graycode), axis = 0)
            nube_de_puntos.append(punto_promedio)

    # Convertir a un array de NumPy para facilitar manipulación
    nube_de_puntos = np.array(nube_de_puntos)
    guardar_nube_de_puntos_ply(nube_de_puntos, "cara_cero_grados.ply")





