import os

ruta = "C:/Users/Ernest/Documents/PruebaOrdenadoReal"
if os.path.exists(ruta):
    print("Contenido real según Python:", os.listdir(ruta))
else:
    print("La ruta no existe para Python.")
