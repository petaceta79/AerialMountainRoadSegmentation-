import cv2
import numpy as np

# Leer imagen
img = cv2.imread('foto.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Obtener dimensiones
alto, ancho = img.shape

# Valores para el sobel
valores = np.zeros_like(img)
media = 0


# Recorrer cada píxel guardando en valores el kernel
for y in range(1, alto-1):       
    for x in range(1, ancho-1):   
        kernel = (img[y-1,x-1].astype(int) + img[y,x-1].astype(int) + img[y+1,x-1].astype(int)) 
        kernel -= (img[y-1,x+1].astype(int) + img[y,x+1].astype(int) + img[y+1,x+1].astype(int))

        kernel = (img[y-1,x-1].astype(int) + img[y-1,x].astype(int) + img[y-1,x+1].astype(int)) 
        kernel -= (img[y+1,x-1].astype(int) + img[y+1,x].astype(int) + img[y+1,x+1].astype(int))

        kernel = abs(kernel)
        valores[y, x] = kernel
        media += kernel

# Calcula la media
media /= (alto-2) * (ancho-2)

# Asigna negro o blanco dependiendo el valor del kernel
img_edit = np.zeros_like(img)

for y in range(1, alto-1):       
    for x in range(1, ancho-1):   
        if (valores[y, x] >= media):
            img_edit[y, x] = 255


# Guardar la imagen resultante
cv2.imwrite('foto_edit.jpg', img_edit)
