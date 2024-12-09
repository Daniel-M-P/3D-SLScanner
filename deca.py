import cv2
import numpy as np
import threading
import glob
import data
from collections import defaultdict

class Camera:
    def __init__(self, position):
        self.position = position # Indica si es la cámara LEFT o RIGHT
        self.matrix = None # Matriz inrínseca
        self.newMatrix = None # Matriz intrínseca undistorted
        self.dist = None # Coeficiente de distorción
        self.rot = None # Matriz de rotación
        self.tras = None # Matriz de traslación

        self.show_corners = False

        # Constantes del archivo data.py
        self.CHESSBOARD_SIZE = data.CHESSBOARD_SIZE
        self.FRAME_SIZE = data.FRAME_SIZE
        self.SIZE_OF_CHESSBOARD_SQUARES_MM = data.SIZE_OF_CHESSBOARD_SQUARES_MM
        self.IMAGES_FOLDER = data.IMAGES_FOLDER
        self.CRITERIA = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    def calibrate(self):
        self.calculate_intrinsics()
        self.calculate_extrinsincs()

    def calculate_intrinsics(self):
        objectPoints, imagePoints = self.chessboard_calibration()
        _, self.matrix, self.dist, rvecs, tvecs = cv2.calibrateCamera(objectPoints, imagePoints, self.FRAME_SIZE, None, None)
        self.tras = np.mean(tvecs, axis = 0)
        matriz_rot = [cv2.Rodrigues(rvec)[0] for rvec in rvecs]
        self.rot = np.mean(matriz_rot, axis=0)
        self.newMatrix, _ = cv2.getOptimalNewCameraMatrix(self.matrix, self.dist, self.FRAME_SIZE, 1, self.FRAME_SIZE)

    def calculate_extrinsincs(self):
        # obj_points1 = np.array(points[0], dtype=np.float32)
        # img_pointsL1 = np.array(points[1], dtype=np.float32).reshape(-1, 2)
        # img_pointsR1 = np.array(points[2], dtype=np.float32).reshape(-1, 2)

        # # Verificar el formato y la cantidad de puntos
        # assert len(obj_points) >= 4, "Se necesitan al menos 4 puntos 3D para solvePnP"
        # assert len(img_pointsL) >= 4, "Se necesitan al menos 4 puntos 2D para solvePnP"
        # assert obj_points.shape[0] == img_pointsL.shape[0], "El número de puntos 3D y 2D debe coincidir"

        # # Resolver el problema PnP

        # _, R_LW, T_LW = cv2.solvePnP(obj_points1, img_pointsL1, newCAML, distL)
        # _, R_RW, T_RW = cv2.solvePnP(obj_points1, img_pointsR1, newCAMR, distR)

        # R_LW, _ = cv2.Rodrigues(R_LW)
        # R_RW, _ = cv2.Rodrigues(R_RW)
        return None

    def chessboard_calibration(self):
        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        objp = np.zeros((self.CHESSBOARD_SIZE[0] * self.CHESSBOARD_SIZE[1], 3), np.float32)
        objp[:,:2] = np.mgrid[0:self.CHESSBOARD_SIZE[0],0:self.CHESSBOARD_SIZE[1]].T.reshape(-1,2)

        # Scale the object points
        objp = objp * self.SIZE_OF_CHESSBOARD_SQUARES_MM

        # Arrays to store object points and image points from all the images.
        objpoints = [] # 3d point in real world space
        imgpoints = [] # 2d points in image plane.

        images = sorted(glob.glob(f'{self.IMAGES_FOLDER}/stereo{self.position}/*.png'))

        for img_png in images:
            img = cv2.imread(img_png)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Find the chess board corners
            ret, corners = cv2.findChessboardCorners(gray, self.CHESSBOARD_SIZE, None)

            # If found, add object points, image points (after refining them)
            if ret == True:
                objpoints.append(objp)
                corners = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), self.CRITERIA)
                imgpoints.append(corners)

                # Draw and display the corners
                if self.show_corners:
                    cv2.drawChessboardCorners(img, self.CHESSBOARD_SIZE, corners, ret)
                    cv2.imshow(f'Cheesboard calibration {self.position}', img)
                    cv2.waitKey(1000)

        cv2.destroyAllWindows()
        return objpoints, imgpoints 

class Deca:
    # Clae que realiza la deconstrucción de los patrones y devuelve un diccionario por ángulo con llave de graycode, siendo 
    # graycode[0] los pixeles de la cámara izquierda asociada a ese código
    # graycode[1] los pixeles de la cámara derecha asociada a ese código
    def __init__(self):
        self.PATTERN_FOLDER = data.PATTERN_FOLDER
        self.ANGLE = 360 // data.TURNS
        self.THRESHOLD = data.THRESHOLD
        self.coordenadas_por_angulo = defaultdict(lambda: defaultdict(lambda: [[], []])) 
        # self.CAML = Camera("Left")
        # self.CAMR = Camera("Right")
        self.sapov2 = True if self.PATTERN_FOLDER == 'sapo5_v2.0' else False
        self.mostrar_mascara = False 

    def procesar_todos_los_angulos(self):
        threads = []
        for angle in range(0, 60, self.ANGLE):  # Puedes ajustar el rango según sea necesario
            thread = threading.Thread(target=self.procesar_coordenadas_por_angulo, args=(f"grados{angle}",))
            threads.append(thread)
            thread.start()

        # Esperar a que todos los hilos terminen
        for thread in threads:
            thread.join()

    def procesar_coordenadas_por_angulo(self, angle):
        for cam in ["cam1", "cam2"]:
            imagen_iluminada_path = f"{self.PATTERN_FOLDER}/{angle}/{cam}/full/full_0.png"
            imagen_oscura_full = f"{self.PATTERN_FOLDER}/{angle}/{cam}/full/full_1.png"

            # Extraer los píxeles no en sombra (coordenadas de los píxeles en la máscara)
            mascara_de_sombra = self.crear_mascarilla_sombra(imagen_iluminada_path, imagen_oscura_full, 1.5, tipo=self.THRESHOLD)
            pixeles_mascara = np.column_stack(np.where(mascara_de_sombra > 0))

            pixel_a_graycode = defaultdict(lambda: [0, 0, 0])  # Usamos defaultdict para evitar try-except
            for pattern_type in ["row", "column"]:
                # Se hace en orden inverso porque saque el orden de las fotos al revés
                rango = range(18, -1, -2) if self.sapov2 else range(9, -1, -1)
                for i in rango:  # Hacerlo dinámico según la cantidad de patrones
                    imagen_patron = f"{self.PATTERN_FOLDER}/{angle}/{cam}/{pattern_type}/{pattern_type}_{i}.png"
                    mascara_patron = self.crear_mascarilla_sombra(imagen_patron, imagen_oscura_full, 3, tipo=self.THRESHOLD)
                    for px, py in pixeles_mascara:
                        gray_bit = 0 if mascara_patron[px, py] == 0 else 1
                        last_binary_bit = pixel_a_graycode[(px, py)][2]
                        # Saque el orden de las fotos al revés, para decodificar el código gray tengo que empezar desde atrás
                        identificador = 18 if self.sapov2 else 9
                        if i == identificador:
                            last_binary_bit = gray_bit

                        else: 
                            last_binary_bit = last_binary_bit ^ gray_bit

                        suma = last_binary_bit * (2 ** (identificador-i))
                        if pattern_type == "row":
                            pixel_a_graycode[(px, py)][0] += suma
                        elif pattern_type == "column":
                            pixel_a_graycode[(px, py)][1] += suma

            for pixel, graycode in pixel_a_graycode.items():
                graycode = tuple(graycode)
                if cam == "cam1":
                    self.coordenadas_por_angulo[f"{angle}"][graycode][0].append(pixel)
                elif cam == "cam2":
                    if graycode not in self.coordenadas_por_angulo[f"{angle}"]:
                        continue
                    if len(self.coordenadas_por_angulo[f"{angle}"][graycode]) == 1:
                        self.coordenadas_por_angulo[f"{angle}"][graycode].append([pixel])
                    else:
                        self.coordenadas_por_angulo[f"{angle}"][graycode][1].append(pixel)

    def crear_mascarilla_sombra(self, imagen_iluminada_path, imagen_oscura_path, k, tipo):
        # Cargar las imágenes en escala de grises usando OpenCV
        img_iluminada = cv2.imread(imagen_iluminada_path, cv2.IMREAD_GRAYSCALE)
        # img_iluminada = cv2.undistort(img_iluminada2, cam_instrinics["matrix"], cam_instrinics["dist"], None, cam_instrinics["newMatrix"])
        img_oscura = cv2.imread(imagen_oscura_path, cv2.IMREAD_GRAYSCALE)
        # img_oscura = cv2.undistort(img_oscura2, cam_instrinics["matrix"], cam_instrinics["dist"], None, cam_instrinics["newMatrix"])

        # Verificar que las imágenes tienen el mismo tamaño
        if img_iluminada.shape != img_oscura.shape:
            raise ValueError("Las imágenes deben tener el mismo tamaño")

        diferencia = cv2.absdiff(img_iluminada, img_oscura)

        if tipo == "otsu":
            # Aplicar Otsu para obtener el threshold óptimo y así una máscara
            _, mascara_no_sombra = cv2.threshold(diferencia, None, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)

        elif tipo == "desviacion":
            # Calcular el promedio y la desviación estándar de la diferencia
            promedio = np.mean(diferencia)
            desviacion = np.std(diferencia)
            
            # Calcular el umbral como el promedio + k veces la desviación estándar
            # k = 3  # Puedes ajustar el valor de k según la sensibilidad que desees
            threshold = promedio + k * desviacion
            _, mascara_no_sombra = cv2.threshold(diferencia, threshold, 255, cv2.THRESH_BINARY)

        if self.mostrar_mascara:
            cv2.imshow("Patron", mascara_no_sombra)
            while True:
                if cv2.waitKey(1) & 0xFF == ord('s'):
                    break

        return mascara_no_sombra
    
def main():
    CAML = Camera("Left")
    CAML.calibrate()
    CAMR = Camera("Right")
    CAMR.calibrate()
    deca = Deca()
    deca.procesar_todos_los_angulos()
    return CAML, CAMR, deca.coordenadas_por_angulo


if __name__ == "__main__":
    CAML, CAMR, coordenadas_por_angulo = main()

