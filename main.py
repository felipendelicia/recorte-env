import cv2
import numpy as np
import os
from tkinter import Tk, filedialog

root = Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.destroy()

# -----------------------------
# Funciones de scanner
# -----------------------------
def ordenar_puntos(pts):
    pts = pts.reshape(4, 2)
    s = pts.sum(axis=1)
    diff = np.diff(pts, axis=1)
    return np.array([
        pts[np.argmin(s)],
        pts[np.argmin(diff)],
        pts[np.argmax(s)],
        pts[np.argmax(diff)]
    ], dtype="float32")


def transformar_perspectiva(img, pts):
    (tl, tr, br, bl) = pts
    width = int(max(np.linalg.norm(br - bl), np.linalg.norm(tr - tl)))
    height = int(max(np.linalg.norm(tr - br), np.linalg.norm(tl - bl)))

    dst = np.array([
        [0, 0],
        [width - 1, 0],
        [width - 1, height - 1],
        [0, height - 1]
    ], dtype="float32")

    M = cv2.getPerspectiveTransform(pts, dst)
    return cv2.warpPerspective(img, M, (width, height))


def escanear(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7, 7), 0)
    edges = cv2.Canny(blur, 50, 150)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
    edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(
        edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    h, w = gray.shape
    area_img = h * w
    contours = [c for c in contours if cv2.contourArea(c) > 0.25 * area_img]

    if not contours:
        return None

    hoja = max(contours, key=cv2.contourArea)
    peri = cv2.arcLength(hoja, True)
    approx = cv2.approxPolyDP(hoja, 0.02 * peri, True)

    if len(approx) != 4:
        return None

    pts = ordenar_puntos(approx)
    return transformar_perspectiva(img, pts)

# -----------------------------
# Seleccionar carpeta
# -----------------------------
root = Tk()
root.withdraw()

input_dir = filedialog.askdirectory(title="Seleccionar carpeta de imágenes")
if not input_dir:
    exit()

output_dir = os.path.join(input_dir, "salida")
os.makedirs(output_dir, exist_ok=True)

imagenes = sorted([
    f for f in os.listdir(input_dir)
    if f.lower().endswith((".jpg", ".jpeg", ".png"))
])

# -----------------------------
# Loop principal
# -----------------------------
for nombre in imagenes:
    path = os.path.join(input_dir, nombre)
    img = cv2.imread(path)
    resultado = escanear(img)

    if resultado is None:
        resultado = img.copy()

    while True:
        cv2.namedWindow("Resultado", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Resultado", screen_width, screen_height)
        cv2.imshow("Resultado", resultado)

        key = cv2.waitKey(0) & 0xFF

        if key == ord("a"):
            cv2.imwrite(os.path.join(output_dir, nombre), resultado)
            break

        elif key == ord("r"):
            cv2.namedWindow("Ajuste manual", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("Ajuste manual", screen_width, screen_height)
            cv2.imshow("Ajuste manual", img)

            # Seleccionar ROI
            roi = cv2.selectROI("Ajuste manual", img, fromCenter=False)
            x, y, w, h = roi
            if w > 0 and h > 0:
                resultado = img[y:y+h, x:x+w]

            cv2.destroyWindow("Ajuste manual")

        elif key == ord("s"):
            break

        elif key == ord("q"):
            cv2.destroyAllWindows()
            exit()

cv2.destroyAllWindows()
print("✔ Proceso terminado")