# roi-videos

El objetivo de esta herramienta en Python es ubicar regiones de interés (ROI) en videos

En este caso, la región de interés será el interior de un rectángulo que resalta una parte de un fotograma (*frame*) del video.

Un punto de partida para este proyecto es la documentación de OpenCv https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html. En particular los siguientes ejemplos (es necesario volver a colocar los tabuladores en los ejemplos):
* Para leer videos. https://docs.opencv.org/4.x/dd/d43/tutorial_py_video_display.html
```import numpy as np
import cv2 as cv
cap = cv.VideoCapture('vtest.avi')
while cap.isOpened():
ret, frame = cap.read()
# if frame is read correctly ret is True
if not ret:
print("Can't receive frame (stream end?). Exiting ...")
break
gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
cv.imshow('frame', gray)
if cv.waitKey(1) == ord('q'):
break
cap.release()
cv.destroyAllWindows()
```
En este caso se utiliza la letra ‘q’ para salir del programa.

*  Para guardar imágenes. https://docs.opencv.org/4.x/db/deb/tutorial_display_image.html
```
import cv2 as cv
import sys
img = cv.imread(cv.samples.findFile("starry_night.jpg"))
if img is None:
sys.exit("Could not read the image.")
cv.imshow("Display window", img)
k = cv.waitKey(0)
if k == ord("s"):
cv.imwrite("starry_night.png", img)

```
En este caso se utiliza la letra ‘s’ para guardar una imagen.

* Para dibujar rectángulos con el ratón. https://docs.opencv.org/4.x/db/d5b/tutorial_py_mouse_handling.html
```
import numpy as np
import cv2 as cv
drawing = False # true if mouse is pressed
mode = True # if True, draw rectangle. Press 'm' to toggle to curve
ix,iy = -1,-1
# mouse callback function
def draw_circle(event,x,y,flags,param):
global ix,iy,drawing,mode
if event == cv.EVENT_LBUTTONDOWN:
drawing = True
ix,iy = x,y
elif event == cv.EVENT_MOUSEMOVE:
if drawing == True:
if mode == True:
cv.rectangle(img,(ix,iy),(x,y),(0,255,0),-1)
else:
cv.circle(img,(x,y),5,(0,0,255),-1)
elif event == cv.EVENT_LBUTTONUP:
drawing = False
if mode == True:
cv.rectangle(img,(ix,iy),(x,y),(0,255,0),-1)
else:
cv.circle(img,(x,y),5,(0,0,255),-1)

img = np.zeros((512,512,3), np.uint8)
cv.namedWindow('image')
cv.setMouseCallback('image',draw_circle)
while(1):
cv.imshow('image',img)
k = cv.waitKey(1) & 0xFF
if k == ord('m'):
mode = not mode
elif k == 27:
break
cv.destroyAllWindows()

```
En este caso ‘m’ permite cambiar el modo.

Quedo atento a sus propuestas para:
* establecer la forma de uso,
* modificar los anteriores ejemplos.

Las propuestas se deben hacer en el enlace de asuntos (*issues*). https://github.com/GerardoMunoz/roi_videos/issues . Siéntase en libertad de crear su propio  asunto o de opinar en los asuntos creados por sus compañeros.



