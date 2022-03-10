import tkinter as tk
from  tkinter import ttk
import cv2 as cv
import csv #import json,

ws  = tk.Tk()
ws.title('Tabla')
ws.geometry('800x400')

humedal_seleccionado = tk.StringVar(value='ninguno')
ttk.Radiobutton(ws,text='Juan Amarillo',value='juan_amarillo',variable=humedal_seleccionado).pack(fill='x',padx=5,pady=5)
ttk.Radiobutton(ws,text='El Tunjo',value='el_tunjo',variable=humedal_seleccionado).pack(fill='x',padx=5,pady=5)
ttk.Radiobutton(ws,text='El Salitre',value='el_salitre',variable=humedal_seleccionado).pack(fill='x',padx=5,pady=5)
ttk.Radiobutton(ws,text='otro',value='otro',variable=humedal_seleccionado).pack(fill='x',padx=5,pady=5)


notebook = ttk.Notebook(ws)
notebook.pack(pady=10, expand=True)
hoja1=ttk.Frame(notebook,width=400,height=280)
hoja2=ttk.Frame(notebook,width=400,height=280)
hoja1.pack(fill='both', expand=True)
hoja2.pack(fill='both', expand=True)
notebook.add(hoja1,text='Seleccionar ROI')
notebook.add(hoja2,text='Humedales')



botones = tk.Frame(hoja1)
botones.pack(side=tk.TOP)

datos=[]

def insertar(dir='falta'):
    global cont,datos
    nombre = dir+'/imagen_'+str(cont)+'.png'
    cont += 1
    escri = cv.imwrite(nombre,recorte) #False#
    if escri:
        item=(str(cont),nombre,dir,humedal_seleccionado.get())
        set.insert(
            parent='',
            index='end',
            iid=cont,
            text='',
            values=item
        )
        datos.append(item)
        
        
        with open('datos.csv','w') as arch:# with open('datos.json','w') as arch:
            csv.writer(arch).writerows(datos)#     arch.write(json.dumps(datos))

    



boton_planta = tk.Button(botones, text="Planta", width=10, height=2, command=lambda :insertar('planta'))
boton_animal = tk.Button(botones, text="Animal", width=10, height=2, command=lambda :insertar('animal'))
boton_planta.pack(in_=botones, side=tk.LEFT)
boton_animal.pack(in_=botones, side=tk.LEFT)


set = ttk.Treeview(hoja1)
set.pack()

set['columns']= ('id', 'archivo','carpeta','humedal')
set.column("#0", width=0,  stretch=tk.NO)
set.heading("id",text="ID",anchor=tk.CENTER)
set.heading("archivo",text="Archivo",anchor=tk.CENTER)
set.heading("carpeta",text="Carpeta",anchor=tk.CENTER)
set.heading("humedal",text="Humedal",anchor=tk.CENTER)

# set.insert(
#     parent='',
#     index='end',
#     iid=0,
#     text='',
#     values=('0','imagen_0','ave')
#     )
# set.insert(parent='',index='end',iid=1,text='',
# values=('1','imagen_1',"flor"))
# set.insert(parent='',index='end',iid=2,text='',
# values=('2','imagen_2','hoja'))
# set.insert(parent='',index='end',iid=3,text='',
# values=('3','imagen_3','roedor'))

cap = cv.VideoCapture('curi2_v2.mp4')


ret, frame = cap.read()
recorte=frame
def repetir_cada_frame():
    global frame,ret
    cv.imshow('frame', frame)
    ret, frame = cap.read()
        # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        #break
        ws.destroy()
        return 
    if cv.waitKey(1) == ord('q'):
        #break
        ws.destroy()
        return 

    #print('hola... otra vez')
    ws.after(33,repetir_cada_frame)

repetir_cada_frame()

cont=0
drawing = False
ix,iy = -1,-1
def roi(event,x,y,flags,param):
    global ix,iy,drawing,cont,recorte
    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y
    elif event == cv.EVENT_MOUSEMOVE:
        if drawing == True:
                cv.rectangle(frame,(ix,iy),(x,y),(0,0,0),1) #quite parametros para poder capturar solo el borde
                pass            
    elif event == cv.EVENT_LBUTTONUP:
        drawing = False
        cv.rectangle(frame,(ix,iy),(x,y),(0,0,0),1)
        if ix != x and iy != y:
            recorte = frame[iy:y,ix:x,:]
            #nombre = 'imagen_'+str(cont)+'.png'
            #cont += 1
            #escri = cv.imwrite(nombre,recorte) #False#
        


cv.namedWindow('frame')
cv.setMouseCallback('frame',roi)


tabla_por_humedal = ttk.Treeview(hoja2)
tabla_por_humedal.pack()

tabla_por_humedal['columns']= ('id', 'archivo','carpeta','humedal')
tabla_por_humedal.column("#0", width=0,  stretch=tk.NO)
tabla_por_humedal.heading("id",text="ID",anchor=tk.CENTER)
tabla_por_humedal.heading("archivo",text="Archivo",anchor=tk.CENTER)
tabla_por_humedal.heading("carpeta",text="Carpeta",anchor=tk.CENTER)
tabla_por_humedal.heading("humedal",text="Humedal",anchor=tk.CENTER)


def cambio_humedal(*args):
    for item in datos:
        if item[-1]==humedal_seleccionado.get():
            tabla_por_humedal.insert(
                parent='',
                index='end',
                iid=int(item[0]),
                text='',
                values=item
            )
            

humedal_seleccionado.trace('w',cambio_humedal)





ws.mainloop()

cap.release()
cv.destroyAllWindows()
