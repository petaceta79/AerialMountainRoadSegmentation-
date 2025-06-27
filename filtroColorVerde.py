import cv2
import numpy as np
from collections import deque

# Elimina manchas del tamaño de tam_minimo
def eliminarManchasPequenas(img, tam_minimo):
    # Alto y ancho de la imagen
    alto, ancho = img.shape

    # Pixel ya visitados
    visitados = np.zeros_like(img, dtype=bool)

    # Aplica BFS para calcular tamaño
    for y in range(alto):
        for x in range(ancho):
            # Aplica BFS a un pixel negro y no visitado 
            if img[y, x] > 0 and not visitados[y, x]:
                # BFS para recolectar los píxeles de esta mancha
                cola = deque()
                cola.append((x, y))
                mancha = [(x, y)]
                visitados[y, x] = True

                # Minetras haya pixeles en la cola continua ( recolectar todos los pixeles )
                while cola:
                    cx, cy = cola.popleft()
                    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                        nx, ny = cx + dx, cy + dy
                        if 0 <= nx < ancho and 0 <= ny < alto:
                            if img[ny, nx] > 0 and not visitados[ny, nx]:
                                visitados[ny, nx] = True
                                cola.append((nx, ny))
                                mancha.append((nx, ny))

                # Depende del tamaño lo elimina o no
                if len(mancha) < tam_minimo:
                    for mx, my in mancha:
                        img[my, mx] = 0

    return img
                
# Elimina pixeles con bajo cantidad de color azul
def Filter_color_azul(img, radi):
    # Separar canales (BGR)
    b, g, r = cv2.split(img)


    # Calcula el umbral minimo para no ser eliminado
    threshold = np.mean(b)
    threshold += threshold*radi

    # Elimina todos los pixeles por debajo del umbral
    b[b < threshold] = 0


    return b

# Aplica el filtro 
def filtro_color_azul_elim(img, div_umbral, restriccion_threshol):
    alto, ancho, _ = img.shape
    img_edit = Filter_color_azul(img, restriccion_threshol)

    size_rem = (alto*ancho) // div_umbral
    img_edit = eliminarManchasPequenas(img_edit, size_rem)

    return img_edit



# Leer imagen
img = cv2.imread('foto1.jpg')

img_edit = filtro_color_azul_elim(img, 16, 0.7)

# Guardar la imagen resultante
cv2.imwrite('foto1_edit.jpg', img_edit)	