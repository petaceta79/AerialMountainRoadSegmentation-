import cv2
import numpy as np
from collections import deque


# calcula el valor en una region de la integral de la imagen
def calcular_region_integral(integral, top, bot, left, right):
    val = integral[bot, right]

    if (left > 0):
        val -= integral[bot, left-1]
    if (top > 0):
        val -= integral[top-1, right]
    if (left > 0 and top > 0):
        val += integral[top-1, left-1]

    return val

# calcula la integral de la imagen con un algoritmo inductivo
def calcualrImgIntegral(img, alto, ancho):
    img_integral = np.zeros(img.shape, dtype=np.int64)
    img_64 = img.astype(np.int64)

    for y in range(alto):       
        for x in range(ancho):  
            img_integral[y, x] = img_64[y, x]
            if (y > 0):
                img_integral[y, x] += img_integral[y-1, x]
            if (x > 0):
                img_integral[y, x] += img_integral[y, x-1]
            if (x > 0 and y > 0):
                img_integral[y, x] -= img_integral[y-1, x-1]

    return img_integral


# aplica una modificacion del filtro sobel
def sobelFilter(img, r):
    # Obtener dimensiones
    alto, ancho = img.shape

    # Calcular integral de la imagen
    img_integral = calcualrImgIntegral(img, alto, ancho)

    # Calculo del sobel
    valores = img.astype(np.int64)
    media = 0

    # Recorre cada pixel aplicando el kernel
    for y in range(r, alto-(r+1)):       
        for x in range(r, ancho-(r+1)):  
            top = y - r
            bottom = y + r
            left = x - r
            right = x + r

            gradiente_x = calcular_region_integral(img_integral, top, bottom, left, x)
            gradiente_x -= calcular_region_integral(img_integral, top, bottom, x, right)
            gradiente_x = abs(gradiente_x)

            gradiente_y = calcular_region_integral(img_integral, top, y, left, right)
            gradiente_y -= calcular_region_integral(img_integral, y, bottom, left, right)
            gradiente_y = abs(gradiente_y)

            kernel = (gradiente_x + gradiente_y)
            valores[y, x] = kernel
            media += kernel

    # Calcula la media
    media /= (alto-(r*2+1)) * (ancho-(r*2+1))

    # Imagen resultado
    img_edit = np.zeros_like(img)

    # Asigna blanco o negro de forma eficiente
    img_edit = np.where(valores >= media, 255, 0).astype(np.uint8)
    
    return img_edit


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

                




# Leer imagen
img = cv2.imread('foto.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


img_edit = sobelFilter(img, 10)
img_edit = eliminarManchasPequenas(img_edit, 0)


# Guardar la imagen resultante
cv2.imwrite('foto_edit.jpg', img_edit)

