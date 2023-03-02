import tkinter as tk
import random
import numpy
from PIL import ImageTk, Image
import time

#+-------------------------------------------+
#GENERACION DE VENTANA Y 2 FRAMES PRINCIPALES
window = tk.Tk()
window.title("JOSE LUIS VERDE")
window.resizable(width=False, height=False)
frameGRID = tk.Frame(master=window, width=80, height=40, bg="white")  #FRAME PARA VISUALIZACION DEL GRID
frameUSER = tk.Frame(master=window, width=150, height=200, bg="white")#FRAME PARA VISUALIZACION DE BOTONES
frameTABLE = tk.Frame(master=window, width=250, height=500, bg="black")
#+-------------------------------------------+
#LOAD DE IMAGENES USADAS
imgluffy = Image.open("./IMAGENES/luffy.png")
luffy = ImageTk.PhotoImage(imgluffy)
imgchest = Image.open("./IMAGENES/chest2.png")
chest = ImageTk.PhotoImage(imgchest)
imggrass = Image.open("./IMAGENES/tierra.png")
grass = ImageTk.PhotoImage(imggrass)
imgwater = Image.open("./IMAGENES/water.png")
water = ImageTk.PhotoImage(imgwater)
imgwall = Image.open("./IMAGENES/bedrock.png")
wall = ImageTk.PhotoImage(imgwall)
imgmagma = Image.open("./IMAGENES/magma.png")
magma = ImageTk.PhotoImage(imgmagma)

#+-------------------------------------------+
#GENERACION DE PRIMER GRID VACIO
for i in range(10):
    for j in range(10):
        label = tk.Label(master=frameGRID, width=8,height=4)
        label.grid(row=i, column=j, padx=2, pady=2)    
frameGRID.pack(fill=tk.BOTH, side=tk.LEFT)                                #MANDAR A LLAMAR AL FRAMEGRID PARA VISUALIZARLO

#+-------------------------------------------+
#INICIALIZACION DE MATRIZ BASE PARA EL GRID
gridA=[[0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0]]

#+-------------------------------------------+
#METODO GENERADOR DE BLOQUES NEGROS PARA FORMAR UN CAMINO
def gen():
    for i in range(10):
        for j in range(10):
            if numpy.random.choice([0,1,0,0,0,0,0,0,0,0]) == 1:         #SE HACE 1/10 PARA DECIDIR SI SE INVIERTE EL 0 A 1
                gridA[i][j]= not gridA[i][j]
            
            if gridA[i][j]==1:                                          #SI PASO EL 1/10 SE DECIDE CADA ADYASENTE CON OTRO 1/10
                if i > 0:                                               #SI SE VAN A INVERTIR CADA UNO
                    if numpy.random.choice([0,1,0,0,0,0,0,0,0,0]) == 1:
                        gridA[i-1][j]= not gridA[i-1][j]
                    
                if i < 9:
                    if numpy.random.choice([0,1,0,0,0,0,0,0,0,0]) == 1:
                        gridA[i+1][j]=not gridA[i+1][j]
                
                if j > 0:
                    if numpy.random.choice([0,1,0,0,0,0,0,0,0,0]) == 1:
                        gridA[i][j-1]=not gridA[i][j-1]

                if j < 9:
                    if numpy.random.choice([0,1,0,0,0,0,0,0,0,0]) == 1:
                        gridA[i][j+1]=not gridA[i][j+1]
    #PRINT DEL TABLERO FINAL DONDE SI ES 1 ES IGUAL A PARED Y SE PONE NEGRO.
    for i in range(10):
        for j in range(10):
            if gridA[i][j]==1:            
                label = tk.Label(master=frameGRID, width=8,height=4, bg="black")
                label.grid(row=i, column=j, padx=2, pady=2)
            else:
                gridA[i][j]=0       #SE VUELVE A DECLARAR PARA EVITAR ERRORES DE STACK
                label = tk.Label(master=frameGRID, width=8,height=4, bg="#CECECE")
                label.grid(row=i, column=j, padx=2, pady=2)
    
#+-------------------------------------------+
#METODO PARA GENERAR AL RATON Y GATO, DONDE CON UN RANDOM SE SELECCIONA CADA AXIS Y SE
#VERIFICA SI ESTA LIBRE. SE MANDA AL GRID PRINCIPAL 2 PARA GATO Y 3 PARA RATON.
def iniciar():
    #CLEAN DE ANTERIOR GATO RATON Y POR DEFECTO TERRENOS.
    for i in range(10):
        for j in range(10):
            if gridA[i][j]==1:            
                label = tk.Label(master=frameGRID, width=58,height=60,image=wall, bg="black")
                label.grid(row=i, column=j, padx=2, pady=2)
            else:
                gridA[i][j]=0       #SE VUELVE A DECLARAR PARA EVITAR ERRORES DE STACK
                label = tk.Label(master=frameGRID, width=58,height=62,image=grass, bg="#E3E3E3")
                label.grid(row=i, column=j, padx=2, pady=2)
    gato=0
    raton=0
    while gato == 0:
        x=random.randint(0,9)
        y=random.randint(0,9)
        if gridA[x][y] == 0:
            gridA[x][y]=2
            label = tk.Label(master=frameGRID, width=58,height=62, image=luffy)
            label.grid(row=x, column=y, padx=2, pady=2)
            gato=1
    while raton == 0:
        x=random.randint(0,9)
        y=random.randint(0,9)
        if gridA[x][y] == 0:
            gridA[x][y]=3
            label = tk.Label(master=frameGRID, width=58,height=62, image=chest, bg="white")
            label.grid(row=x, column=y, padx=2, pady=2)
            raton=1
    piso()

#+-------------------------------------------+
#COMANDO PARA LIMPIAR EL GRID EN CASO DE GENERAR GRID IMPOSIBLE DE SOLUCIONAR
#(METODO TEMPORAL EN LO QUE SE IMPLEMENTA UN VERIFICADOR)
def clean():
    for i in range(10):
        for j in range(10):
            gridA[i][j]=0
            label = tk.Label(master=frameGRID, width=8,height=4, bg="#CECECE")
            label.grid(row=i, column=j, padx=2, pady=2)

#+-------------------------------------------+
#METODO PARA GENERAR DIFERENTES TIPO DE CAMINOS
#4 = PASTO | 5 = AGUA
def piso():
    for i in range(10):
        for j in range(10):
            #SI ES BLANCO TIENE 1/20 DE CAMBIAR EL TERRENO
            if gridA[i][j]==1:
                if numpy.random.choice([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]) == 1:
                    gridA[i][j]=random.randint(4,5)
            #SI ES NEGRO TIENE 1/10 DE CAMBIAR DE TERRENO
            if gridA[i][j]==0:
                if numpy.random.choice([0,1,0,0,0,0,0,0,0,0]) == 1:
                    gridA[i][j]=random.randint(4,5)
            #AQUI MISMO SE EVITA QUE SE GENERE EN POSICIONES DE RATON O GATO (2,3)
            if gridA[i][j]==4:
                label = tk.Label(master=frameGRID, width=58,height=62, image=magma, bg="green")
                label.grid(row=i, column=j, padx=2, pady=2)
            elif gridA[i][j]==5:
                label = tk.Label(master=frameGRID, width=58,height=62,image=water, bg="blue")
                label.grid(row=i, column=j, padx=2, pady=2)

#+-------------------------------------------+
#METODO PARA BUSQUEDA DE CASILLA MAS ECONOMICA
def busqueda():
    #[0]NORMAL,[1]PARED,[2]GATO,[3]RATON,[4]PASTO,[5]AGUA
    costos=[1,50,5,0,3,4]
    #P=D+H+C  | D ES DISTANCIA DE NODO | H CANTIDAD NODOS A OBJETIVO | C COSTO |
    #SACAR POSICION RATON Y GATO
    rv=[0,0]
    gb=[0,1]
    for i in range(10):
        for j in range(10):
            if gridA[i][j] == 3:
                rv[0]=i
                rv[1]=j
            if gridA[i][j] == 2:
                gb[0]=i
                gb[1]=j
    print(gb,rv)
    #SACAR DISTANCIA INICIAL
    dini=(abs(gb[0]-rv[0])+abs(gb[1]-rv[1]))
    print(dini)
    dact=dini
    listn=[]
    postxt=str(gb[0])+","+str(gb[1])
    listn=[str(postxt)]
    while dact != 0:
        #CASO DE NO TENER, LIMPIAR
        dsup=99
        dinf=99
        dizq=99
        dder=99
        #VERFICAR ARRIBA
        print("#-----")
        if gb[0] > 0:
            dsup=(abs(gb[0]-1-rv[0])+abs(gb[1]-rv[1]))
            dirsig=str(gb[0]-1)+","+str(gb[1])
            print("SUPERIOR: ",dirsig)
            if dsup > dact:
                dsup = dsup + 4
            if dirsig in listn:
                dsup = dsup + 5
            costsig = gridA[gb[0]-1][gb[1]]
            dsup = costos[costsig] + dsup
        #VERIFICAR ABAJO
        if gb[0] < 9:
            dinf=(abs(gb[0]+1-rv[0])+abs(gb[1]-rv[1]))
            dirsig=str(gb[0]+1)+","+str(gb[1])
            print("INFERIOR: ",dirsig)
            if dinf > dact:
                dinf = dinf + 4
            if dirsig in listn:
                dinf = dinf + 5
            costsig =  gridA[(gb[0]+1)][gb[1]]
            dinf = costos[costsig] + dinf
        #VERIFICAR IZQUIERDA
        if gb[1] > 0:
            dizq=(abs(gb[0]-rv[0])+abs(gb[1]-1-rv[1]))
            dirsig=str(gb[0])+","+str(gb[1]-1)
            print("IZQUIERDA: ",dirsig)
            if dizq > dact:
                dizq = dizq + 4
            if dirsig in listn:
                dizq = dizq + 5
            costsig = gridA[gb[0]][gb[1]-1]
            dizq = costos[costsig] + dizq
        #VERIFICAR DERECHA
        if gb[1] < 9:
            dder=(abs(gb[0]-rv[0])+abs(gb[1]+1-rv[1]))
            dirsig=str(gb[0])+","+str(gb[1]+1)
            print("DERECHA: ",dirsig)
            if dder > dact:
                dder = dder + 4
            if dirsig in listn:
                dder = dder + 5
            costsig = gridA[gb[0]][gb[1]+1]
            dder = costos[costsig] + dder
        print("superior: ",dsup," inferior: ",dinf," izquierda: ", dizq," derecha: ",dder)
        #CLEAN DEL LUFFY
        label = tk.Label(master=frameGRID, width=58,height=62,image=grass, bg="#E3E3E3")
        label.grid(row=gb[0], column=gb[1], padx=2, pady=2)
        gridA[gb[0]][gb[1]]=0
        #CAMBIO DE POSICION
        print("POSICION PRE MOV: ",gb[0],gb[1])
        print("DISTANCIA PRE MOV: ",dact)
        print("DIRECCION DEL MOV: ")
        gb[0],gb[1] = costover(dsup,dinf,dizq,dder,gb[0],gb[1])
        label = tk.Label(master=frameGRID, width=58,height=62,image=luffy, bg="#E3E3E3")
        label.grid(row=gb[0], column=gb[1], padx=2, pady=2)
        gridA[(gb[0])][gb[1]]=2
        postxt=str(gb[0])+","+str(gb[1])
        listn.append(postxt)
        print(listn)
        #CHECK COSTOS
        #window.after(850)
        #frameGRID.after(800)
        dact=(abs(gb[0]-rv[0])+abs(gb[1]-rv[1]))
        print("POSICION POST MOV: ",gb[0],gb[1])
        print("DISTANCIA POST MOV: ",dact)
        #time.time(50)
        
        

def costover(dsup,dinf,dizq,dder,gb,gb2):
    min_num = dsup
    if dinf < min_num:
        min_num = dinf
    if dizq < min_num:
        min_num = dizq
    if dder < min_num:
        min_num = dder

    #SELECTOR ALEATORIO DE A DONDE MOVERSE
    sel=random.randint(0,1)
    if dsup == min_num:
        if dsup == dinf:
            if sel:
                print("dsupinf")
                return(gb+1,gb2)
        if dsup == dizq:
            if sel:
                print("dsupizq")
                return(gb,gb2-1) 
        if dsup == dder:
            if sel:
                print("dsupdder")
                return(gb,gb2+1)
    if dinf == min_num:
        if dinf == dizq:
            if sel:
                print("dinfizq")
                return(gb,gb2-1) 
        if dinf == dder:
            if sel:
                print("dinfdder")
                return(gb,gb2+1)
    if dizq == min_num:
        if dizq == dder:
            if sel:
                print("dizqdder")
                return(gb,gb2+1)
    print("SELFALT")
    #SELECTOR FALTANTE
    if min_num == dsup:
        print("SUP")
        return(gb-1,gb2)
    elif min_num == dinf:
        print("INF")
        return(gb+1,gb2)
    elif min_num == dizq:
        print("IZQ")
        return(gb,gb2-1)    
    else:
        print("DER")
        return(gb,gb2+1)
#+-------------------------------------------+
#BOTONES
generar=tk.Button(master=frameUSER, text="GENERAR", command=gen, bd=0, bg="white")
generar.place(y=15,relx=.5,anchor="center")
cursor=tk.Button(master=frameUSER, text="INICIAR", command=iniciar, bd=0, bg="white")
cursor.place(y=45,relx=.5,anchor="center")
#terreno=tk.Button(master=frameUSER, text="TERRENOS", command=piso, bd=0, bg="white")
#terreno.place(y=85,x=50)
mover=tk.Button(master=frameUSER, text="MOVER", command=busqueda, bd=0, bg="white")
mover.place(y=75,relx=.5,anchor="center")
limpiar=tk.Button(master=frameUSER, text="LIMPIAR", command=clean, bd=0, bg="white")
limpiar.place(y=105,relx=.5,anchor="center")
info=tk.Label(master=frameUSER,text="COSTOS\nTIERRA=1\nMAGMA=3\nAGUA=4\nBACKWRD=+4",bg="white",fg="grey")
info.place(y=160,relx=.5,anchor="center")
frameUSER.pack(fill=tk.X, expand=False,anchor="n")
frameTABLE.pack(fill=tk.BOTH, expand=False,anchor="se")
window.mainloop()
