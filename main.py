
import numpy as np
import cv2
from sys import getsizeof

ancho_imagen = 512  # 1920 #
alto_imagen = 512  # 863 #

# Lee las propiedades del video 
NOMBRE_VIDEO = 'curi2_v2.mp4'
cap = cv2.VideoCapture(NOMBRE_VIDEO)
ancho_video = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))   
alto_video = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  
num_colores = 3 # se asume que el video está en colores (Blue, Gren, Red)
fps = cap.get(cv2.CAP_PROP_FPS)
num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print('alto y ancho de cada frame', alto_video, ancho_video)
print('fps, número de frames, duración', fps, num_frames, num_frames/fps)

# Calcula nuevas dimensiones del video para ahorrar memoria 
if alto_imagen/alto_video > ancho_imagen/ancho_video:
    alto_imagen = alto_video*ancho_imagen//ancho_video
else:
    ancho_imagen = ancho_video*alto_imagen//alto_video
video_shape = (num_frames,
               alto_imagen, ancho_imagen, num_colores)
video = np.empty(video_shape, dtype=np.uint8)
print('ancho_imagen,alto_imagen', ancho_imagen, alto_imagen)

# Se leen todos los frames para poder avanzar o retroceder libremente
# desafortunadamente esto consume mucha memoria
print('iniciando leer', video_shape[0], 'frames')
i = 0
ret = cap.isOpened()
while ret:
    ret, frame = cap.read()
    if ret:
        frame = cv2.resize(frame, (ancho_imagen, alto_imagen),
                           interpolation=cv2.INTER_AREA)
        cv2.putText(frame,
                    '  tecla_d:avanza frame,  tecla_a:retrocede frame, drag:selecciona sub-imagen y guarda el archivo',
                    (0, 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.3,
                    (0, 0, 0),
                    1)
        video[i, ...] = frame
        i += 1
        if i % 100 == 0:
            print('van', i, 'frames')

cap.release()
print('creado el arreglo de numpy')
print('sus dimensiones son: num frames, alto, ancho, colores(RGB)', video.shape)
print('ocupa en memoria', getsizeof(video), 'bytes')

# Se crea un callback para determinar las dimensiones del rectángulo
# definido con el mouse mediante el drag 
drawing = False
ix, iy = -1, -1
jx, jy = -1, -1
def draw_rect(event, x, y, flags, param):
    global ix, iy, jx, jy, drawing
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
    elif event == cv2.EVENT_MOUSEMOVE:
        jx, jy = x, y
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        roi = video[indice, iy:jy, ix:jx, :]
        print('roi', roi.shape, ix, jx, iy, jy)
        cv2.imwrite("roi.png", roi)
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_rect)




# Se realiza un ciclo para actualizar los frames según los fps
# y estar pendiente del teclado y los callbacks
indice = 0
max_indice = video.shape[0] - 1
while(1):
    img = np.copy(video[indice, ...])
    if drawing == True:
        cv2.rectangle(img, (ix, iy), (jx, jy), (0, 0, 255), 2)
    cv2.imshow('image', img)
    k = cv2.waitKey(int(1000/fps))
    if k == ord('d'):
        indice += 1
        if indice > max_indice:
            indice = 0
    elif k == ord('a'):
        indice -= 1
        if indice < 0:
            indice = max_indice
    elif k == 27:
        break

# Finalizado el ciclo se cierran las ventanas
cv2.destroyAllWindows()
