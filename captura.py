import cv2
import numpy as np
from google.colab import files
import matplotlib.pyplot as plt

# Cargar la imagen
# Sube tu imagen a Colab primero
uploaded = files.upload()
image_name = list(uploaded.keys())[0]
img = cv2.imread(image_name)

# Convertir a escala de grises
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Aplicar un filtro gaussiano para reducir el ruido
blurred = cv2.GaussianBlur(gray, (9, 9), 2)

# Detectar círculos usando HoughCircles
circles = cv2.HoughCircles(
    blurred,
    cv2.HOUGH_GRADIENT,
    dp=1,
    minDist=100,
    param1=50,
    param2=30,
    minRadius=200,  # Ajusta este valor según el tamaño del círculo que quieres detectar
    maxRadius=400   # Ajusta este valor según el tamaño del círculo que quieres detectar
)
#zona 1: Radio: 376
#zona2: Radio: 206
#zona3:Radio: 103
#zona4: Radio: 53
#            1: {'minRadius': 360, 'maxRadius': 380},   # Imagen 1: círculos pequeños
#            2: {'minRadius': 190, 'maxRadius': 215},  # Imagen 2: círculos medianos
#            3: {'minRadius': 90, 'maxRadius': 110},  # Imagen 3: círculos grandes
#            4: {'minRadius': 40, 'maxRadius': 60}   # Imagen 4: círculos muy grandes
#
# Si se encuentran círculos
zona1 = 376
zona2 = 206  # Reducción: 170 píxeles (45.2%)
zona3 = 103  # Reducción: 103 píxeles (50.0%)
zona4 = 53   # Reducción: 50 píxeles (48.5%)

if circles is not None:
    circles = np.uint16(np.around(circles))
    
    # Dibujar el círculo más grande
    largest_circle = circles[0][0]  # Tomar el primer círculo detectado
    center = (largest_circle[0], largest_circle[1])
    radius = largest_circle[2]
    
    # Dibujar el círculo en rojo
    cv2.circle(img, center, radius, (0, 0, 255), 2)
    
    # Imprimir las coordenadas y el radio para ajuste
    print(f"Centro: {center}, Radio: {radius}")

# Mostrar el resultado
plt.figure(figsize=(15,15))
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()