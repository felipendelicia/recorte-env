import os
import cv2
from scanner.core import escanear
from scanner.gui import seleccionar_carpeta, abrir_ventana_maximized, ajustar_manual
from tkinter import Tk

# Obtener tamaño de pantalla
root = Tk()
screen_size = (root.winfo_screenwidth(), root.winfo_screenheight())
root.destroy()

# Seleccionar carpeta
input_dir = seleccionar_carpeta()
if not input_dir:
    exit()

output_dir = os.path.join(input_dir, "salida")
os.makedirs(output_dir, exist_ok=True)

# Listar imágenes
imagenes = sorted([f for f in os.listdir(input_dir) if f.lower().endswith((".jpg", ".jpeg", ".png"))])

# Loop principal
for nombre in imagenes:
    path = os.path.join(input_dir, nombre)
    img = cv2.imread(path)

    # Escaneo automático
    resultado = escanear(img)
    if resultado is None:
        resultado = img.copy()

    while True:
        abrir_ventana_maximized("Resultado", resultado, screen_size)
        key = cv2.waitKey(0) & 0xFF

        if key == ord("a"):  # Guardar
            cv2.imwrite(os.path.join(output_dir, nombre), resultado)
            break

        elif key == ord("r"):  # Ajuste manual
            resultado = ajustar_manual(img, screen_size)

        elif key == ord("s"):  # Saltar
            break

        elif key == ord("q"):  # Salir
            cv2.destroyAllWindows()
            exit()

cv2.destroyAllWindows()
print("✔ Proceso terminado")